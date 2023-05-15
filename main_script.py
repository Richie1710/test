import os
from git import Repo
import time
import logging
from gitlab_helper import create_gitlab_merge_request
from gitea_helper import create_gitea_pull_request

# Get the log level from the environmental variable or set it to INFO by default
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

def create_merge_request(source_repo_url: str, destination_repo_url: str, destination_path: str) -> None:
    """
    Create a merge request or pull request based on the destination repository type.

    Args:
        source_repo_url (str): The URL of the source repository.
        destination_repo_url (str): The URL of the destination repository.
        destination_path (str): The local path of the destination repository.

    """
    # Clone the source repository
    logger.info(f"Cloning source repository: {source_repo_url}")
    source_repo = Repo.clone_from(source_repo_url, '/tmp/source_repo')

    # Clone or open the destination repository
    try:
        logger.info(f"Opening destination repository: {destination_path}")
        destination_repo = Repo(destination_path)
    except:
        logger.info(f"Cloning destination repository: {destination_repo_url}")
        destination_repo = Repo.clone_from(destination_repo_url, destination_path)

    # Get the last commit of both repositories
    source_commit = source_repo.head.commit.hexsha
    destination_commit = destination_repo.head.commit.hexsha

    if source_commit != destination_commit:
        branch_name = f"branch_{int(time.time())}"  # Generate branch name with Unix timestamp
        # Checkout the destination repository to the source commit and create a new branch
        logger.info(f"Checking out to source commit: {source_commit}")
        destination_repo.git.checkout(source_commit, b=branch_name)
        logger.info(f"Checked out to the source commit and created a new branch: {branch_name}")

        # Create a merge request or pull request in the destination repository
        if 'gitlab' in destination_repo_url:
            logger.info("Creating merge request in GitLab...")
            merge_request_url = create_gitlab_merge_request(destination_repo_url, branch_name)
            if merge_request_url:
                logger.info(f"Merge request created in GitLab: {merge_request_url}")
            else:
                logger.error("Failed to create merge request in GitLab.")
        elif 'gittea' in destination_repo_url:
            logger.info("Creating pull request in Gitea...")
            pull_request_url = create_gitea_pull_request(destination_repo_url, branch_name)
            if pull_request_url:
                logger.info(f"Pull request created in Gitea: {pull_request_url}")
            else:
                logger.error("Failed to create pull request in Gitea.")
        else:
            logger.error("Unsupported destination repository platform.")

    else:
        logger.info("The last commits are the same. No merge request necessary.")

if __name__ == '__main__':
    source_url = 'https://github.com/source_user/source_repository.git'
    destination_gitlab_url = 'https://gitlab.com/destination_user/destination_repository.git'
    destination_gitea_url = 'https://gitea.com/destination_user/destination_repository.git'
    destination_path = '/path/to/destination/repository'

    logger.info("Running the main script...")
    create_merge_request(source_url, destination_gitlab_url, destination_path)
    create_merge_request(source_url, destination_gitea_url, destination_path)

