import logging
import re
from io import BytesIO
from json import dumps, loads
from pathlib import Path
from zipfile import ZipFile

import requests
from github import Github
from github.GitRelease import GitRelease

from create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

BUNDLE_REPO = "adafruit/Adafruit_CircuitPython_Bundle"
BUNDLES_PATH = Path.cwd() / "bundles"


def filename_sanitize(filename: str) -> str:
    """
    Sanitize a filename. Found https://stackoverflow.com/a/13593932/10291933

    :param filename: A string.
    :return: A string. 
    """
    return re.sub("[^\w\-_\. ]", "_", filename)


def directory_sanitize(filename: str) -> str:
    """
    Sanitize a directory. Found https://stackoverflow.com/a/13593932/10291933

    :param filename: A string.
    :return: A string.
    """
    return re.sub("[^\w\-_\. ]", "_", filename).replace(".", "_")


class GitHubManager:
    def __init__(self, token: str):
        """
        Make a GitHub manager.

        :param token: The token to use to authenticate with the GitHub APIs.
        """
        self.token = token
        logger.debug("Authenticating with GitHub")
        self.github = Github(token)

    def get_bundle_releases(self) -> list[GitRelease]:
        """
        Get all the bundle releases and return a list of them.

        :return: A list of github.GitRelease.GitRelease
        """
        logger.debug("Getting repo...")
        repo = self.github.get_repo(BUNDLE_REPO)
        logger.debug("Getting releases...")
        return list(repo.get_releases())

    def download_release(self, release: GitRelease):
        """
        Download a release into the bundle folder.

        :param release: A GitRelease to download from.
        """
        # To test, I used this code: (Make sure you have GitHub token stored in
        # CredentialManager!)
        #
        # from bundle_manager import BundleManager
        # from github_manager import GitHubManager
        # bm = BundleManager()
        # gm = GitHubManager(bm.cred_manager.get_github_token())
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
        BUNDLES_PATH.mkdir(exist_ok=True)
        path = BUNDLES_PATH / directory_sanitize(release.title)
        logger.debug(f"Path to new bundle is {path}")
        path.mkdir()
        if len(list(path.iterdir())) > 0:
            raise FileExistsError("Bundle already exists!")
        for asset in assets:
            url = asset.browser_download_url
            logger.debug(f"Downloading {url}")
            response = requests.get(url)
            response.raise_for_status()
            if url.endswith(".zip"):
                zip_data = BytesIO()
                zip_data.write(response.content)
                logger.debug(f"Extracting zip file")
                with ZipFile(zip_data) as zip_f:
                    zip_f.extractall(path)
            else:
                file_path = path / filename_sanitize(url.split("/")[-1])
                file_path.write_bytes(response.content)
        bundles = []
        dependencies = {}
        for thing in path.glob("*"):
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
        metadata_path.write_text(dumps(bundle_metadata, indent=2))
