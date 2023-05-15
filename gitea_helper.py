import requests

def create_gitea_pull_request(destination_repo_url: str, branch_name: str) -> str:
    """
    Create a pull request in Gitea repository.

    Args:
        destination_repo_url (str): The URL of the Gitea repository.
        branch_name (str): The name of the branch to create the pull request.

    Returns:
        str: The URL of the created pull request.

    """
    api_url = destination_repo_url.replace('.git', '/api/v1')
    headers = {'Content-Type': 'application/json'}
    data = {
        'title': f'Merge {branch_name}',
        'body': f'Pull request for branch: {branch_name}',
        'source_branch': branch_name,
        'target_branch': 'master',  # Adjust the target branch as per your requirements
    }
    response = requests.post(f"{api_url}/pulls", json=data, headers=headers)
    if response.status_code == 201:
        pull_request = response.json()
        return pull_request['html_url']
    else:
        return None

