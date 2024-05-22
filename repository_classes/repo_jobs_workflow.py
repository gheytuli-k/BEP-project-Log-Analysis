from repository_classes import RequestFromRepo
import requests 
from http import HTTPStatus

class RepoJobsWorkflow(RequestFromRepo):
    

    def get_info(self) -> None:
        """
        Prints all the request attributes.
        
        :return: None
        """

        pass

    def set_request_info(self, *args, **kwargs) -> None:
        """
        Set the request information
        
        :return: None 
        """

        self.repo_owner = kwargs.get("repo_owner")
        self.repo_name = kwargs.get("repo_name")
        self.workflow_id = kwargs.get("workflow_id")

    def make_request(self) -> None:
        """
        Makes a request to the repository with the set request information.
        
        :return: None
        """

        pass


    def make_request(self) -> None:
        """
        Makes a request to retrieve the jobs within one workflow from the repository.

        :return: None
        """

        endpoint = f"repos/{self.repo_owner}/{self.repo_name}/actions/runs/{self.workflow_id}/jobs"
        # headers = {
        #     'Authorization': f'token {self.AUTHENTICATION_KEY}',
        #     'Accept': 'application/vnd.github.v3.raw'
        # }

        self.response = requests.get(f"{self.GITHUB_API_URL}/{endpoint}")
        self.update_jobs_info()
        self.status_code = HTTPStatus(self.response.status_code).value
        self.status_phrase = HTTPStatus(self.response.status_code).phrase
        self.status_description = HTTPStatus(
            self.response.status_code).description

    def update_jobs_info(self) -> None:
        """
        Update the jobs information from the response.

        :return: None
        """
        jobs = []

        for job in self.response.json().get("jobs"):
            job_info = {}
            job_info["name"] = job.get("name")
            job_info["run_id"] = job.get("run_id")
            job_info["status"] = job.get("status")
            job_info["conclusion"] = job.get("conclusion")
            success_steps = []
            failure_steps = []

            for step in job.get("steps"):
                if step.get("conclusion") == "success":
                    success_steps.append(step.get("name"))
                else:
                    failure_steps.append(step.get("name"))
            
            job_info["success_steps"] = success_steps
            job_info["failure_steps"] = failure_steps
            jobs.append(job_info)

        self.jobs = jobs

