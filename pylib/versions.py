"""Docstring for the versions.py module.

Represents different software versions.

"""
# Standard Library Imports
import enum
import re

# Third Party Imports

# Local Application Imports


class NoJenkinsVersionFoundError(ValueError):
    """Represent when a Jenkins version cannot be found."""


class VersionUpdateTypes(enum.Enum):
    """Represent values that designate type of software versioning update."""

    MAJOR = enum.auto()
    MINOR = enum.auto()
    PATCH = enum.auto()
    RESEAT = enum.auto()


class Version:
    """Represent a generic software version."""

    @classmethod
    def determine_greatest_update_type(self, versions):
        """Determine the greatest version update type passed in.

        Parameters
        ----------
        versions : list of autotag.VersionUpdateTypes
            A list of VersionUpdateTypes objects.

        Returns
        -------
        autotag.VersionUpdateTypes or None
            The greatest update type, or None if versions is empty.

        """
        greatest = None

        # major > minor > patch
        for version in versions:
            if version == VersionUpdateTypes.RESEAT and (
                greatest != VersionUpdateTypes.PATCH
                and greatest != VersionUpdateTypes.MINOR  # noqa: W503
                and greatest != VersionUpdateTypes.MAJOR  # noqa: W503
            ):
                pass
            elif version == VersionUpdateTypes.PATCH and (
                greatest != VersionUpdateTypes.MINOR
                and greatest != VersionUpdateTypes.MAJOR  # noqa: W503
            ):
                greatest = VersionUpdateTypes.PATCH
            elif version == VersionUpdateTypes.MINOR and (
                greatest != VersionUpdateTypes.MAJOR
            ):
                greatest = VersionUpdateTypes.MINOR
            elif version == VersionUpdateTypes.MAJOR:
                greatest = VersionUpdateTypes.MAJOR

        return greatest

    def determine_update_types(self, v1):
        """Determine the version update types between another version.

        Parameters
        ----------
        v1 : autotag.Version
            A version object.

        Returns
        -------
        list of autotag.VersionUpdateTypes

        Notes
        -----
        When going from one (software) version to another. It's normal to
        consider whether the new version is considered a patch, minor, or major
        update to the previous version.

        """
        update_types = list()
        if abs(self.major - v1.major) > 0:
            update_types.append(VersionUpdateTypes.MAJOR)
        if abs(self.minor - v1.minor) > 0:
            update_types.append(VersionUpdateTypes.MINOR)
        if abs(self.patch - v1.patch) > 0:
            update_types.append(VersionUpdateTypes.PATCH)

        return update_types


class SemanticVersion(Version):
    """Represent a semantic version.

    Parameters
    ----------
    version : str
        A semantic version string (e.g. 1.2.3, 3.2.2).

    Attributes
    ----------
    SEMANTIC_VERSION_REGEX : str
        The regex used to extract the different parts of the semantic
        versioning.

    """

    _MAJOR_CAPTURE_GROUP = 1
    _MINOR_CAPTURE_GROUP = 2
    _PATCH_CAPTURE_GROUP = 3

    # for reference on where I got this regex from:
    # https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
    SEMANTIC_VERSION_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"  # noqa: E501

    def __init__(self, version):
        """Construct the semantic version object."""
        semantic_groups = re.match(self.SEMANTIC_VERSION_REGEX, version)
        self.major = int(semantic_groups[self._MAJOR_CAPTURE_GROUP])
        self.minor = int(semantic_groups[self._MINOR_CAPTURE_GROUP])
        self.patch = int(semantic_groups[self._PATCH_CAPTURE_GROUP])

    def set_major(self, to):
        """Set the semantic versioning major to a given version.

        Parameters
        ----------
        to : int
            The version to set the semantic versioning major to.

        """
        self.major = to

    def set_minor(self, to):
        """Set the semantic versioning minor to a given version.

        Parameters
        ----------
        to : int
            The version to set the semantic versioning minor to.

        """
        self.minor = to

    def set_patch(self, to):
        """Set the semantic versioning patch to a given version.

        Parameters
        ----------
        to : int
            The version to set the semantic versioning patch to.

        """
        self.patch = to

    def increment_major(self, by):
        """Increment the semantic versioning major by a given amount.

        Parameters
        ----------
        by : int
            The amount to increment the semantic versioning major by.

        """
        self.major += by

    def increment_minor(self, by):
        """Increment the semantic versioning minor by a given amount.

        Parameters
        ----------
        by : int
            The amount to increment the semantic versioning minor by.

        """
        self.minor += by

    def increment_patch(self, by):
        """Increment the semantic versioning patch by a given amount.

        Parameters
        ----------
        by : int
            The amount to increment the semantic versioning patch by.

        """
        self.patch += by

    def __eq__(self, v):
        """Determine if the semantic version is equal to this instance."""
        return (
            f"{self.major}.{self.minor}.{self.patch}"
            == f"{v.major}.{v.minor}.{v.patch}"  # noqa: W503
        )

    def __str__(self):
        """Return the string representation of an instance."""
        return f"{self.major}.{self.minor}.{self.patch}"


class JenkinsVersion(Version):
    """Represent a Jenkins version.

    Parameters
    ----------
    version : str
        A Jenkins version string (e.g. 1.2.3, 3.2.2).

    Attributes
    ----------
    JENKINS_VERSION_REGEX : str
        The regex used to extract the different parts of the Jenkins
        versioning.

    """

    _MAJOR_CAPTURE_GROUP = 1
    _MINOR_CAPTURE_GROUP = 2
    _PATCH_CAPTURE_GROUP = 3
    _IMPLICIT_PATCH_CHANGE_VERSION = -1

    # based on the semantic version regex
    _ENV_VAR_REGEX = r"^[a-zA-Z_]\w*=.+"
    _JENKINS_VERSION_ENV_VAR_NAME = "JENKINS_VERSION"
    JENKINS_VERSION_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"  # noqa: E501

    def __init__(self, version):
        """Construct the Jenkins version object."""
        version_groups = re.match(self.JENKINS_VERSION_REGEX, version)
        self.major = int(version_groups[self._MAJOR_CAPTURE_GROUP])
        self.minor = int(version_groups[self._MINOR_CAPTURE_GROUP])
        self.patch = version_groups[self._PATCH_CAPTURE_GROUP]

        if not self.patch:
            # I still want to always detect a patch version update regardless
            # of what this version ever gets compared to. This is unless only
            # a minor to minor version update occurs (e.g. 2.333 -> 2.334).
            self.patch = self._IMPLICIT_PATCH_CHANGE_VERSION
        else:
            self.patch = int(self.patch)

    @classmethod
    def from_docker_image(cls, docker_client, docker_image):
        """Construct a version from a Jenkins Docker image.

        Parameters
        ----------
        docker_client : docker.client.DockerClient
            The Docker client object.
        docker_image : str
            The qualified Docker image name.

        Returns
        -------
        versions.JenkinsVersion

        Raises
        ------
        NoJenkinsVersionFoundError
            If the Jenkins version cannot be found in the Docker image.

        """
        # There does not currently appear to be a way to examine a Docker image
        # without pulling the image first. At least through Docker's Python
        # SDK.
        jenkins_env_vars = docker_client.images.pull(docker_image).attrs[
            "Config"
        ]["Env"]
        docker_client.images.remove(docker_image)

        for env_var in jenkins_env_vars:
            regex = re.compile(cls._ENV_VAR_REGEX)
            if regex.search(env_var) and (
                cls._JENKINS_VERSION_ENV_VAR_NAME  # noqa: W503
                == env_var.split("=")[0]  # noqa: W503
            ):
                return cls(env_var.split("=")[1])

        raise NoJenkinsVersionFoundError(
            "No Jenkins version found in Docker image"
        )

    def __eq__(self, v):
        """Determine if the Jenkins version is equal to this instance."""
        return (
            f"{self.major}.{self.minor}.{self.patch}"
            == f"{v.major}.{v.minor}.{v.patch}"  # noqa: W503
        )

    def __str__(self):
        """Return the string representation of an instance."""
        return (
            f"{self.major}.{self.minor}"
            if self.patch == self._IMPLICIT_PATCH_CHANGE_VERSION
            else f"{self.major}.{self.minor}.{self.patch}"
        )
