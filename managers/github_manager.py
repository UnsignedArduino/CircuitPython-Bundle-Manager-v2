import logging
from io import BytesIO
from typing import Callable
from helpers.file_size import ByteSize
from json import dumps, loads
from pathlib import Path
from zipfile import ZipFile

import requests
from github import Github
from github.GitRelease import GitRelease

from helpers.create_logger import create_logger
from helpers.sanitizers import filename_sanitize, directory_sanitize
from helpers.singleton import Singleton

logger = create_logger(name=__name__, level=logging.DEBUG)


class GitHubManager(metaclass=Singleton):
    def __init__(self, token: str, bundle_repo: str, bundle_path: Path):
        """
        Make a GitHub manager.

        :param token: The token to use to authenticate with the GitHub APIs.
        :param bundle_repo: The repo to download releases from.
        :param bundle_path: The path to where bundles are stored.
        """
        self.token = token
        self.bundle_repo = bundle_repo
        self.bundle_path = bundle_path
        logger.debug("Authenticating with GitHub")
        self.github = Github(token)

    def get_bundle_releases(self, pb_func: Callable) -> list[GitRelease]:
        """
        Get all the bundle releases and return a list of them.

        :param pb_func: A function to call to update GUIs, etc. Will be passed
         2 ints positionally with the first being how far and the second being
         the total.
        :return: A list of github.GitRelease.GitRelease
        """
        logger.debug("Getting repo...")
        repo = self.github.get_repo(self.bundle_repo)
        logger.debug("Getting releases...")
        pag_list = repo.get_releases()
        releases = []
        total = pag_list.totalCount
        for index, item in enumerate(pag_list):
            pb_func(index, total)
            releases.append(item)
        logger.debug(f"Got {len(releases)} GitReleases")
        return releases

    def download_release(self, release: GitRelease, pb_func: Callable):
        """
        Download a release into the bundle folder.

        :param release: A GitRelease to download from.
        :param pb_func: A function to call to update GUIs, etc. WIll be passed
         2 integers and a string positionally with the first being how far,
         the second being the toital, and the third being a status bar.
        """
        # To test, I used this code: (Make sure you have GitHub token stored in
        # CredentialManager!)
        #
        # from pathlib import Path
        #
        # BUNDLES_PATH = Path.cwd() / "bundles"
        # BUNDLE_REPO = "adafruit/Adafruit_CircuitPython_Bundle"
        #
        # from circuitpython_bundle_manager import CircuitPythonBundleManager
        # from managers.github_manager import GitHubManager
        # cpybm = CircuitPythonBundleManager()
        # gm = GitHubManager(cpybm.cred_manager.get_github_token(),
        #                    BUNDLE_REPO, BUNDLES_PATH)
        # releases = gm.get_bundle_releases()
        # gm.download_release(releases[0])
        logger.debug(f"Downloading {release}")
        assets = list(release.get_assets())
        bundle_metadata = {
            "title": release.title,
            "tag_name": release.tag_name,
            "url": release.html_url,
            "released": release.published_at.timestamp()
        }
        self.bundle_path.mkdir(exist_ok=True)
        path = self.bundle_path / directory_sanitize(release.title)
        logger.debug(f"Path to new bundle is {path}")
        path.mkdir()
        if len(list(path.iterdir())) > 0:
            raise FileExistsError("Bundle already exists!")
        for asset in assets:
            url = asset.browser_download_url
            logger.debug(f"Downloading {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total = int(response.headers["Content-Length"].strip())
            got = 0
            if url.endswith(".zip"):
                zip_data = BytesIO()
                for chunk in response.iter_content(chunk_size=1024):
                    got += len(chunk)
                    status = f"Downloading ZIP file - " \
                             f"{str(ByteSize(got))} / " \
                             f"{str(ByteSize(total))}"
                    pb_func(got, total, status)
                    zip_data.write(chunk)
                logger.debug(f"Extracting zip file")
                pb_func(1, 1, f"Extracting ZIP file...")
                with ZipFile(zip_data) as zip_f:
                    zip_f.extractall(path)
            elif url.endswith(".json"):
                file_path = path / filename_sanitize(url.split("/")[-1])
                status = f"Downloading JSON file (" \
                         f"{str(ByteSize(total))})"
                pb_func(1, 1, status)
                file_path.write_bytes(response.content)
            else:
                file_path = path / filename_sanitize(url.split("/")[-1])
                for chunk in response.iter_content(chunk_size=1024):
                    got += len(chunk)
                    status = f"Downloading file - " \
                             f"{str(ByteSize(got))} / " \
                             f"{str(ByteSize(total))}"
                    pb_func(got, total, status)
                    file_path.write_bytes(chunk)
        bundles = []
        dependencies = {}
        total = len(list(path.glob("*")))
        for index, thing in enumerate(path.glob("*")):
            logger.debug(f"Scanning {thing}")
            pb_func(index + 1, total, f"Scanning downloaded content... "
                                      f"({index + 1} / {total})")
            if "mpy" in thing.name or "py" in thing.name and \
                    "examples" not in thing.name and thing.is_dir():
                logger.debug(f"Found bundle: {thing}")
                bundles.append(str(thing))
            if "json" in thing.name and thing.is_file():
                logger.debug(f"Found dependencies file: {thing}")
                dependencies = loads(thing.read_text())
        bundle_metadata["bundles"] = bundles
        bundle_metadata["dependencies"] = dependencies
        metadata_path = path / "metadata.json"
        logger.debug(f"Writing metadata to {metadata_path}")
        pb_func(1, 1, "Writing metadata...")
        metadata_path.write_text(dumps(bundle_metadata, indent=2))
