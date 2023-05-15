import gitlab

def create_gitlab_merge_request(destination_repo_url: str, branch_name: str) -> str:
    """
    Create a merge request in GitLab repository.

    Args:
        destination_repo_url (str): The URL of the GitLab repository.
        branch_name (str): The name of the branch to create the merge request.

    Returns:
        str: The URL of the created merge request.

    """

    private_token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not private_token:
        raise ValueError("GitLab private token not found in environmental variables.")

    gl = gitlab.Gitlab('https://gitlab.com', private_token=orivate_token)
    project_id = destination_repo_url.split('/')[-2]  # Extract project ID from URL
    project = gl.projects.get(project_id)
    merge_request = project.mergerequests.create({
        'source_branch': branch_name,
        'target_branch': 'master',  # Adjust the target branch as per your requirements
        'title': f'Merge {branch_name}',
        'description': f'Merge request for branch: {branch_name}',
    })
    return merge_request.web_url

