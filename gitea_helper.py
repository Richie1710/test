import requests
import logging

logger = logging.getLogger(__name__)

def create_gitea_pull_request(destination_repo_url: str, branch_name: str) -> str:
    """
    Create a pull request in Gitea repository.

    Args:
        destination_repo_url (str): The URL of the Gitea repository.
        branch_name (str): The name of the branch to create the pull request.

    Returns:
        str: The URL of the created pull request.

    """
    # Make the API request to create a pull request
    api_url = f"{destination_repo_url}/api/v1/repos/{destination_repo_url.split('/')[-1]}/pulls"
    response = requests.post(api_url, json={"head": branch_name, "base": "master"})
    
    if response.status_code == 201:
        pull_request = response.json()
        logger.info(f"Pull request created in Gitea: {pull_request['html_url']}")
        return pull_request['html_url']
    else:
        logger.error("Failed to create pull request in Gitea.")
        return None

