"""
CircuitPython Bundle Manager v2 - a Python program to easily manage
modules on a CircuitPython device!

Copyright (C) 2021 UnsignedArduino

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from io import BytesIO
from json import dumps, loads
from pathlib import Path
from typing import Callable
from zipfile import ZipFile

import requests
from github import Github
from github.GitRelease import GitRelease

from helpers.create_logger import create_logger
from helpers.file_size import ByteSize
from helpers.sanitizers import filename_sanitize, directory_sanitize

logger = create_logger(name=__name__, level=logging.DEBUG)

github_instance = None


class GitHubManager:
    def __init__(self, token: str, bundle_repo: str, bundle_path: Path,
                 is_community: bool = False):
        """
        Make a GitHub manager.

        :param token: The token to use to authenticate with the GitHub APIs.
        :param bundle_repo: The repo to download releases from.
        :param bundle_path: The path to where bundles are stored.
        :param is_community: A bool on whether this repo is the community
         bundle or not.
        """
        self.token = token
        self.bundle_repo = bundle_repo
        self.bundle_path = bundle_path
        self.is_community = is_community
        global github_instance
        if github_instance is None:
            logger.debug("Authenticating with GitHub")
            self.github = Github(token)
            github_instance = self.github
        else:
            logger.debug(f"Using existing authenticated GitHub object")
            self.github = github_instance
        logger.debug("Getting repo...")
        self.repo = self.github.get_repo(self.bundle_repo)
        logger.debug("Getting releases...")
        self.release_pag = self.repo.get_releases()
        self.max_page = int(self.release_pag._getLastPageUrl().split("?page=")[1])

    def download_release(self, release: GitRelease, pb_func: Callable):
        """
        Download a release into the bundle folder.

        :param release: A GitRelease to download from.
        :param pb_func: A function to call to update GUIs, etc. Will be passed
         2 integers and a string positionally with the first being how far,
         the second being the total, and the third being a status bar.
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
            "title": release.title + (" (community)" if self.is_community else ""),
            "tag_name": release.tag_name,
            "url": release.html_url,
            "released": release.published_at.timestamp()
        }
        self.bundle_path.mkdir(exist_ok=True)
        path = self.bundle_path / directory_sanitize(
            release.title + (" (community)" if self.is_community else "")
        )
        logger.debug(f"Path to new bundle is {path}")
        path.mkdir()
        for asset in assets:
            url = asset.browser_download_url
            logger.debug(f"Downloading {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total = int(response.headers["Content-Length"].strip())
            got = 0
            if url.endswith(".zip"):
                zip_data = BytesIO()
                for chunk in response.iter_content(chunk_size=1024 * 64):
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
