import requests
from http import HTTPStatus
from typing import List


class RepoCommits:
    """
    A class for interacting with a repository's commit history.

    This class provides methods to fetch commits from a repository
    within a specified date range.

    ----------

    Attributes:
        repo_owner : str
            The owner of the repository
        repo_name : str
            The name of the repository
        branch_name : str
            The name of the branch. Default is "main"
        since : str
            The start date for filtering commits. Default is None
        until : str
            The end date for filtering commits. Default is None
        per_page : int
            The number of commits to retrieve per page. Default is 100
        page : int
            The page number of commits to retrieve. Default is 1
    """

    def __init__(self, repo_owner: str = None, repo_name: str = None, branch_name: str = "main", since: str = None, until: str = None, per_page: int = 100, page: int = 1) -> None:
        """
        Build a RepoCommits instance with the specified attributes.
        :param repo_owner: The owner of the repository
        :param repo_name: The name of the repository
        :param branch_name: The name of the branch
        :param since: The start date for filtering commits
        :param until: The end date for filtering commits
        :param per_page: The number of commits to retrieve per page
        :param page: The page number of commits to retrieve
        :return: None
        """

        pass

    def _make_request(self) -> None:
        """
        Makes a request to retrieve the commits from the repository.
        """

        pass

    def get_report(self):
        """
        Returns a report of the commits retrieved.
        """

        pass

    def get_response_code(self) -> HTTPStatus:
        """
        Returns the HTTP status code of the request.
        :return: HTTPStatus
        """

        pass

    def get_response_code_message(self) -> str:
        """
        Returns the message associated with the HTTP status code.
        :return: str
        """

        pass

    def get_commits_ids(self) -> List[str]:
        """
        Returns a list of commit IDs.
        :return: List[str]
        """

        pass
