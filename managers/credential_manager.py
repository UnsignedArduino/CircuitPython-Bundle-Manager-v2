import logging
from typing import Union

import keyring

from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class CredentialManager:
    def __init__(self, service_name: str, github_token_name: str):
        """
        Make a CredentialManager.

        :param service_name: The name of the service.
        :param github_token_name: The username for storing and reading the
         GitHub token.
        """
        self.service_name = service_name
        self.github_token_name = github_token_name
        self.github_token = None

    def set_github_token(self, token: str, save_in_keyring: bool = True):
        """
        Set the GitHub token that is used.

        :param token: The token to set.
        :param save_in_keyring: Whether to save it in the OS' credential
         manager.
        """
        self.github_token = token
        if save_in_keyring:
            logger.debug("Saving token to OS' credential manager")
            keyring.set_password(self.service_name, self.github_token_name,
                                 token)

    def get_github_token(self) -> Union[str, None]:
        """
        Get the GitHub token that is used. If one is already set in memory,
        we will use that, otherwise we will try to load it from the OS'
        credential manager, otherwise None.

        :return: A str or None.
        """
        logger.debug("Obtaining GitHub token")
        if self.github_token is not None:
            return self.github_token
        else:
            return keyring.get_password(self.service_name,
                                        self.github_token_name)

    def has_github_token(self, in_keyring: bool = False) -> bool:
        """
        Get whether we have a GitHub token in memory or stored in the OS'
        credential manager.

        :param in_keyring: Whether to check only the OS' credential manager
         for a token.
        :return: A bool.
        """
        if in_keyring:
            return keyring.get_password(self.service_name,
                                        self.github_token_name) is not None
        else:
            return self.github_token is not None or \
                   keyring.get_password(self.service_name,
                                        self.github_token_name) is not None

    def delete_github_token(self):
        """
        Delete the GitHub token from the OS' credential manager.
        """
        logger.debug("Deleting GitHub token")
        keyring.delete_password(self.service_name, self.github_token_name)
