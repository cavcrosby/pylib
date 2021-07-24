"""Docstring for the githubauth.py module.

Holds the class that implements authentication to GitHub.

"""
# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports


class GitHubAuth(requests.auth.AuthBase):
    """Custom HTTPBasicAuth for GitHub.

    Instead of using a username/password pair, this HTTPBasicAuth subclass
    uses personal access tokens to authenticate with GitHub. For reference:
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api#authentication

    Parameters
    ----------
    access_token : str
        Used to authenticate through GitHub's REST API.

    """

    def __init__(self, access_token):
        """Instantiate GitHubAuth class.

        Parameters
        ----------
        access_token : str
            This is a personal access token that you generate from GitHub.

        """
        self.access_token = access_token

    def __call__(self, prepared_requests_obj):
        """Set prepared request object with the apprioate header value.

        Parameters
        ----------
        access_token : str
            Typically this is a personal access token that you can generate
            from GitHub.

        Returns
        ----------
        prepared_requests_obj : requests.models.PreparedRequest
            The prepared request object with the access token attached.

        """
        prepared_requests_obj.headers[
            "Authorization"
        ] = self.auth_header_value()
        return prepared_requests_obj

    def auth_header_value(self):
        """Part of OAuth2 authentication.

        See the following link:
        https://developer.github.com/v3/#oauth2-token-sent-in-a-header

        """
        return f"token {self.access_token}"
