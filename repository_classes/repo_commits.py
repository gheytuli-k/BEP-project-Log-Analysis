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

    GITHUB_API_URL = "https://api.github.com"
    status_code = 0
    status_phrase = ""
    status_description = "No request made yet"

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

        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.since = since
        self.until = until
        # self.per_page = per_page
        # self.page = page

    def _make_request(self) -> None:
        """
        Makes a request to retrieve the commits from the repository.
        """

        endpoint = f"repos/{self.repo_owner}/{self.repo_name}/commits"
        params = {
            "sha": self.branch_name,
            "since": self.since,
            "until": self.until,
            # "per_page": self.per_page,
            # "page": self.page
        }

        self.response = requests.get(
            f"{self.GITHUB_API_URL}/{endpoint}", params=params)
        self.status_code = HTTPStatus(self.response.status_code).value
        self.status_phrase = HTTPStatus(self.response.status_code).phrase
        self.status_description = HTTPStatus(
            self.response.status_code).description

    def get_report(self) -> None:
        """
        Returns a report of the commits retrieved.
        """

        assert self.status_code != 0, "No request made yet, call _make_request() first"
        assert self.status_code == 200, "Request failed, check status code"
        data = self.response.json()
        if len(data) == 0:
            return "No commits found"
        else:
            for commit in data:
                commit_id = commit['sha']
                commit_parent_id = commit['parents'][0]['sha']
                commit_message = commit['commit']['message']
                commit_timestamp = commit['commit']['author']['date']

                print(f"Commit ID: {commit_id}\nParent ID: {commit_parent_id}\nMessage: {commit_message}\nTimestamp: {commit_timestamp}\n\n")

    def get_response_code(self) -> int:
        """
        Returns the HTTP status code of the request.
        :return: HTTPStatus
        """

        return self.status_code

    def get_response_code_phrase(self) -> str:
        """
        Returns the phrase associated with the HTTP status code.
        :return: str
        """

        return self.status_phrase

    def get_response_code_description(self) -> str:
        """
        Returns the message associated with the HTTP status code.
        :return: str
        """

        return self.status_description

    def get_commits_ids(self) -> List[str]:
        """
        Returns a list of commit IDs.
        :return: List[str]
        """

        assert self.status_code != 0, "No request made yet, call _make_request() first"
        assert self.status_code == 200, "Request failed, check status code"
        data = self.response.json() 
        commits = [commit["sha"] for commit in data]
        return commits
