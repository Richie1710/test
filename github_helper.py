import requests

def create_github_pull_request(destination_repo_url: str, branch_name: str) -> str:
    """
    Create a pull request in a GitHub repository.

    Args:
        destination_repo_url (str): The URL of the GitHub repository.
        branch_name (str): The name of the branch to create the pull request.

    Returns:
        str: The URL of the created pull request.

    """
    # Extract the owner and repository name from the destination repository URL
    owner, repo_name = extract_owner_repo(destination_repo_url)

    # Create a pull request in the GitHub repository
    endpoint = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "Bearer YOUR_GITHUB_ACCESS_TOKEN"
    }
    data = {
        "title": f"Pull request from {branch_name}",
        "head": branch_name,
        "base": "main"
    }

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 201:
        pull_request_url = response.json().get("html_url")
        return pull_request_url

    return None

def extract_owner_repo(repo_url: str) -> tuple[str, str]:
    """
    Extract the owner and repository name from a GitHub repository URL.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        tuple[str, str]: The owner and repository name.

    """
    parts = repo_url.split("/")
    owner = parts[-2]
    repo_name = parts[-1].split(".")[0]  # Remove the '.git' extension
    return owner, repo_name

