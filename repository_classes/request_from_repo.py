from abc import ABC, abstractmethod


class RequestFromRepo(ABC):
    """
    Abstract class for requests to repository    

    Attributes:
    ----------
    task : str
        brief task description
    """

    GITHUB_API_URL = "https://api.github.com"
    status_code = 0
    status_phrase = ""
    status_description = "No request made yet"

    def __init__(self, task: str) -> None:
        """
        Build a RequestFromRepo instance with the specified attributes.
        :param task: brief task description
        :return: None
        """
        self.task = task

    def get_response_code(self) -> int:
        """
        Return the status code of the response
        """
        return self.status_code

    def get_response_phrase(self) -> str:
        """
        Return the status phrase of the response
        """
        return self.status_phrase

    def get_response_description(self) -> str:
        """
        Return the status description of the response
        """
        return self.status_description

    @abstractmethod
    def get_info(self) -> None:
        """
        Print the instance information
        """
        pass

    @abstractmethod
    def set_request_info(self, *args, **kwargs):
        """
        Set request information
        """
        pass

    @abstractmethod
    def make_request(self) -> None:
        """
        Makes a request to the repository with the set request information
        """
        pass
