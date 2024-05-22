from repository_classes import RequestFromRepo
import requests
from http import HTTPStatus
from typing import List, Dict
import os

class RepoWorkflow(RequestFromRepo):

    AUTHENTICATION_KEY = ""

    def get_info(self) -> None:
        """
        Prints all the request attributes.
        """
        print(f"Repository Owner: {self.repo_owner}")
        print(f"Repository Name: {self.repo_name}")
        print(f"Branch Name: {self.branch_name}")
        print(f"Since: {self.since}")
        print(f"Until: {self.until}")
        print(f"Per Page: {self.per_page}")
        print(f"Page: {self.page}")

    def set_request_info(self, *args, **kwargs) -> None:
        """
        set the request information

        :param repo_owner: The owner of the repository 
        :param repo_name: The name of the repository
        :param branch_name: The name of the branch
        :param since: The start date for filtering commits
        :param until: The end date for filtering commits
        :param per_page: The number of commits to retrieve per page
        :param page: The page number of commits to retrieve
        :return: None
        """

        self.repo_owner = kwargs.get("repo_owner")
        self.repo_name = kwargs.get("repo_name")
        self.branch_name = kwargs.get("branch_name")
        self.since = kwargs.get("since")
        self.until = kwargs.get("until")
        self.per_page = kwargs.get("per_page")
        self.page = kwargs.get("page")

    def make_request(self) -> None:
        """
        Makes a request to retrieve the Workflows from the repository.

        :return: None
        """

        endpoint = f"repos/{self.repo_owner}/{self.repo_name}/actions/runs"
        params = {
            "sha": self.branch_name,
            "since": self.since,
            "until": self.until,
            # "per_page": self.per_page,
            # "page": self.page
        }

        self.response = requests.get(
            f"{self.GITHUB_API_URL}/{endpoint}", params=params)
        self.update_workflow_info()
        self.status_code = HTTPStatus(self.response.status_code).value
        self.status_phrase = HTTPStatus(self.response.status_code).phrase
        self.status_description = HTTPStatus(
            self.response.status_code).description

    def update_workflow_info(self) -> None:
        """
        Update the workflow information.

        :return: None
        """
        failed_workflows = []
        successful_workflows = []

        for workflow in self.response.json()['workflow_runs']:
            workflow_information = {}
            
            workflow_information['name'] = workflow['name']
            workflow_information['id'] = workflow['id']
            workflow_information['status'] = workflow['status']
            workflow_information['conclusion'] = workflow['conclusion']
            workflow_information['path'] = workflow['path']
            workflow_information['event'] = workflow['event']
            workflow_information['created_at'] = workflow['created_at']
            workflow_information['url'] = workflow['url']
            workflow_information['jobs_url'] = workflow['jobs_url']
            workflow_information['logs_url'] = workflow['logs_url']

            if workflow['conclusion'] == 'failure':
                failed_workflows.append(workflow_information)
            else:
                successful_workflows.append(workflow_information)

        self.nr_of_workflows = self.response.json()['total_count']
        self.failed_workflows = failed_workflows
        self.successful_workflows = successful_workflows

    def get_successful_workflows(self) -> List[Dict]:
        """
        Get the successful workflows.

        :return: List[Dict]
        """

        return self.successful_workflows

    def get_failed_workflows(self) -> List[Dict]:
        """
        Get the failed workflows.

        :return: List[Dict]
        """

        return self.failed_workflows

    def get_workflow_info(self) -> None:
        """
        Get information about the workflows in the request made.
        
        :return: None
        """

        print(f"Total count of workflows: {self.response.json()['total_count']}")
        