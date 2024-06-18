from repository_classes import *
from typing import Dict, List
import zipfile
from necessary_functions import output_diff
from necessary_functions import unzip
from necessary_functions import setup_prompt_env, send_prompt
import os

def get_workflows(repo_owner, repo_name, branch_name, start_date, end_date) -> None:
    start_date = ""
    end_date = ""

    # Getting the failed workflows in the specified time range
    workflows = RepoWorkflow("Get workflow")
    workflows.set_request_info(repo_owner="gheytuli-k", repo_name="calculadora-tk-bep", branch_name="main", page=1, per_page=1000)
    workflows.make_request()
    workflows.update_workflow_info()
    failed_workflows = workflows.get_failed_workflows()
    successful_workflows = workflows.get_successful_workflows()

    return failed_workflows, successful_workflows

def get_jobs_in_workflow(repo_owner, repo_name, workflow_id, storing_path, auth_key) -> None:
    jobs = RepoJobsWorkflow("Get jobs in workflow that had already a successful run")
    jobs.set_request_info(repo_owner="gheytuli-k", repo_name="calculadora-tk-bep", workflow_id=workflow_id, page=1, per_page=200)
    jobs.make_request()
    print('failed steps: ')
    print(jobs.get_failed_jobs())
    
    jobs.store_runs_logs(storing_path, auth_key)
    print(f'storing the logs at {storing_path}'+'\\logs\\zipped\\'+f'{str(workflow_id)}')
    
    return jobs

def concatenate_logs(destination):
    all_logs = ""
    for root, dirs, files in os.walk(destination):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf8') as f:
                all_logs += f"Log's of {file}:\n{f.read()}\n"
    return all_logs

def feeding_gemini_api(message):
    convo = setup_prompt_env()
    return send_prompt(message, convo)

def pipeline_implementation():
    auth_key = "key"

    storing_path = 'C:\\University\\Year 3\\Q4\\BEP\\Calc\\calculadora-tk-bep'

    failed_workflows, successful_workflows = get_workflows("gheytuli-k", "calculadora-tk-bep", "master", "", "")
    for failed_workflow in failed_workflows:
        print(failed_workflow["id"])
        for successful_workflow in successful_workflows:
            if failed_workflow["id"] == 9480393158 and successful_workflow["id"] == 9480508112:
                if failed_workflow["name"] == successful_workflow["name"]:

                    print(f"Workflow: {failed_workflow['name']}")
                    print(f"Failed at: {failed_workflow['created_at']}")
                    print(f"Successful at: {successful_workflow['created_at']}")
                    print()

                    jobs = get_jobs_in_workflow("gheytuli-k", "BEP-project-Log-Analysis", failed_workflow["id"], storing_path, auth_key)

                    source = f"{storing_path}\\logs\\zipped\\{str(failed_workflow['id'])}.zip"
                    destination = f"{storing_path}\\logs\\unzipped\\{str(failed_workflow['id'])}"
                    unzip(source, destination, jobs.get_failed_jobs())
                    successful_head = successful_workflow['head_sha']
                    failed_head = failed_workflow['head_sha']
                    concatenated_logs = concatenate_logs(destination)

                    output_diff(destination, successful_head, failed_head)

                    with open(f"{destination}/diff_output.txt", 'r') as f:
                        diff_output = f.read()
                        diff_output = "Differences between the successful run and failed run repository state\n"+diff_output

                    print(concatenated_logs + diff_output)
                    
                    print(feeding_gemini_api(concatenated_logs + diff_output))






                
                





        # else:
        #     print(f"Workflow: {failed_workflow['name']}")
        #     print(f"Failed at: {failed_workflow['created_at']}")
        #     print(f"Successful at: None")
        #     print("\n")

        #     jobs = RepoJobsWorkflow("Get jobs in workflow")
        #     jobs.set_request_info(repo_owner="gheytuli-k", repo_name="BEP-project-Log-Analysis", workflow_id=failed_workflow["id"])
        #     jobs.make_request()

        #     print('failed steps:')
        #     print(jobs.get_failed_jobs())

        #     print(f'storing the logs at {storing_path}'+'\\logs\\zipped\\'+f'{str(failed_workflow["id"])}')

        #     jobs.store_runs_logs(storing_path, auth_key)

        #     source = f"{storing_path}\\logs\\zipped\\{str(failed_workflow['id'])}.zip"
        #     destination = f"{storing_path}\\logs\\unzipped\\{str(failed_workflow['id'])}"
        #     unzip(source, destination, jobs.get_failed_jobs())
        
        
        







pipeline_implementation()


# # Specify the repository path
# repo_path = 'C:\\University\\Year 3\\Q4\\BEP\\BEP-project-Log-Analysis'

# # Specify the two commits or branches to compare
# commit1 = '8cede0769035f94050dd85f14e68368fe6cab8dd'
# commit2 = 'd2d4b4b9bb3040b7f83f9d4afea729e0ab5cc282'

# output_diff(repo_path, commit1, commit2)

# # read the file diff_output.txt and store it in a variable
# with open('diff_output.txt', 'r') as f:
#     diff_output = f.read()

# # Print the contents of the file
# print(diff_output)

# print(concatenate_logs("C:\\University\\Year 3\\Q4\\BEP\\BEP-project-Log-Analysis\\logs\\unzipped\\9401391647"))