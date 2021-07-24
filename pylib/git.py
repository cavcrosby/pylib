"""Docstring for the git.py module.

Contains custom functionality using the third party git package.

"""
# Standard Library Imports
import os

# Third Party Imports
import git

# Local Application Imports


def is_git_repo(path):
    """Determine if path passed in is a git repository.

    Returns
    -------
    bool
        If the path is a git repository.

    """
    try:
        git.Repo(path, search_parent_directories=True).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def get_git_working_dir():
    """Determine the nearest git working directory.

    This is relative to the cwd (current working directory).

    Returns
    -------
    str
        The path of the nearest git working directory. An empty string will be
        return if the git repo path determined is to a bare git repo.

    Raises
    ------
    git.exc.InvalidGitRepositoryError
        If a git repo could not be found relative to the cwd.

    """
    cwd = os.getcwd()
    try:
        return git.Repo(cwd, search_parent_directories=True).working_tree_dir
    except git.exc.InvalidGitRepositoryError as except_obj:
        except_obj.args = (cwd,)
        raise except_obj
