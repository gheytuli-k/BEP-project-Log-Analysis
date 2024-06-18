import requests
from http import HTTPStatus


class RepoBranch:
    """
    Retrieve information about a repository branch.
    """

    GITHUB_API_URL = "https://api.github.com"
    status_code = 0
    status_phrase = ""
    status_description = "No request made yet"

    def __init__(self, owner:str, repo:str) -> None:
        """
        Build a RepoBranch instance with the specified attributes.
        :param owner: The owner of the repository
        :param repo: The name of the repository
        :return: None
        """

        self.owner = owner
        self.repo = repo

    def _make_request(self) -> None:
        """
        Makes a request to retrieve all the branch from the repository.
        :param branch: The name of the branch
        """

        endpoint = f"repos/{self.owner}/{self.repo}/branches"
        self.response = requests.get(f"{self.GITHUB_API_URL}/{endpoint}")
        self.status_code = HTTPStatus(self.response.status_code).value
        self.status_phrase = HTTPStatus(self.response.status_code).phrase
        self.status_description = HTTPStatus(self.response.status_code).description

    def get_all_branches(self) -> dict:
        """
        Retrieve all branches in the repository.
        :return: A dictionary of branches in the repository
        """

        assert self.status_code != 0, "No request made yet, call _make_request() first"
        assert self.status_code == 200, "Request failed, check status code"
        
        branches = self.response.json()
        return [{"name": branch["name"], "commit_sha": branch["commit"]["sha"]} for branch in branches]
    