#!/usr/bin/env python3
# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports


class GitHubAuth(requests.auth.AuthBase):
    """Custom HTTPBasicAuth for GitHub.

    GitHub does not require a username and password to use their API. Instead
    an API token is used. For reference:
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api#authentication

    Parameters
    ----------
    api_token : str
        Used to authenticate through GitHub's REST API.

    """

    def __init__(self, api_token):

        self.api_token = api_token

    def __call__(self, requests_obj):

        requests_obj.headers["Authorization"] = self.auth_header_value()
        return requests_obj

    def auth_header_value(self):
        """Part of OAuth2 authentication.

        See the following link:
        https://developer.github.com/v3/#oauth2-token-sent-in-a-header

        """
        return f"token {self.api_token}"
