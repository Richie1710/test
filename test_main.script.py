import unittest
from unittest.mock import patch, MagicMock
from git import Repo
from main_script import create_merge_request

class TestMainScript(unittest.TestCase):

    def test_create_merge_request_same_commit(self):
        with patch('main_script.Repo') as mock_repo:
            mock_source_repo = MagicMock()
            mock_destination_repo = MagicMock()
            mock_repo.clone_from.side_effect = [mock_source_repo, mock_destination_repo]
            mock_source_repo.head.commit.hexsha = 'abcdef'
            mock_destination_repo.head.commit.hexsha = 'abcdef'

            with patch('main_script.create_gitlab_merge_request') as mock_create_gitlab_mr:
                with patch('main_script.create_gitea_pull_request') as mock_create_gitea_pr:
                    create_merge_request('source_url', 'destination_url', 'destination_path')

                    self.assertEqual(mock_repo.clone_from.call_count, 2)
                    self.assertEqual(mock_repo.git.checkout.call_count, 0)
                    self.assertEqual(mock_create_gitlab_mr.call_count, 0)
                    self.assertEqual(mock_create_gitea_pr.call_count, 0)

    def test_create_merge_request_different_commit(self):
        with patch('main_script.Repo') as mock_repo:
            mock_source_repo = MagicMock()
            mock_destination_repo = MagicMock()
            mock_repo.clone_from.side_effect = [mock_source_repo, mock_destination_repo]
            mock_source_repo.head.commit.hexsha = 'abcdef'
            mock_destination_repo.head.commit.hexsha = '123456'

            with patch('main_script.create_gitlab_merge_request') as mock_create_gitlab_mr:
                with patch('main_script.create_gitea_pull_request') as mock_create_gitea_pr:
                    create_merge_request('source_url', 'destination_url', 'destination_path')

                    self.assertEqual(mock_repo.clone_from.call_count, 2)
                    self.assertEqual(mock_repo.git.checkout.call_count, 1)
                    self.assertEqual(mock_create_gitlab_mr.call_count, 1)
                    self.assertEqual(mock_create_gitea_pr.call_count, 0)

if __name__ == '__main__':
    unittest.main()
