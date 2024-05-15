from repository_classes import RequestFromRepo

class LimitRateStatus(RequestFromRepo):
    """
    A class for interacting with the GitHub API rate limit status.
    """

    def get_info(self) -> None:
        """
        Prints all the request attributes.
        """

        pass

    def set_request_info(self, *args, **kwargs) -> None:
        """
        Set request information
        """

        pass

    def make_request(self) -> None:
        """
        Makes a request to the repository with the set request information
        """

        pass