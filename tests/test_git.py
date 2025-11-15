import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from os import environ
from anilist_readme.git import git_check_activity, git_config, git_add_commit_push


class TestGitCheckActivity(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.original_dev = environ.get("DEV")
        environ["DEV"] = "true"  # Prevent actual git commands
    
    def tearDown(self):
        """Clean up test environment"""
        if self.original_dev is None:
            environ.pop("DEV", None)
        else:
            environ["DEV"] = self.original_dev
    
    @patch('anilist_readme.git.syscmd')
    def test_git_check_activity_with_recent_commit(self, mock_syscmd):
        """Test that git_check_activity doesn't commit when commit is recent"""
        # Mock git log to return a recent commit (1 day ago)
        recent_date = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        mock_syscmd.return_value = recent_date
        
        git_check_activity("token", "email@example.com", "username")
        
        # Should not create a dummy commit
        commit_calls = [call for call in mock_syscmd.call_args_list 
                       if len(call[0]) > 0 and 'commit --allow-empty' in str(call[0][0])]
        self.assertEqual(len(commit_calls), 0)
    
    @patch('anilist_readme.git.syscmd')
    def test_git_check_activity_with_old_commit(self, mock_syscmd):
        """Test that git_check_activity checks for old commit correctly"""
        # Mock git log to return an old commit (60 days ago)
        old_date = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
        
        def syscmd_side_effect(cmd, *args, **kwargs):
            if 'log' in cmd and 'pretty=format' in cmd:
                return old_date
            return 0
        
        mock_syscmd.side_effect = syscmd_side_effect
        
        git_check_activity("token", "email@example.com", "username")
        
        # Should call syscmd for git log
        log_calls = [call for call in mock_syscmd.call_args_list 
                    if len(call[0]) > 0 and 'log' in str(call[0][0]) and 'pretty=format' in str(call[0][0])]
        self.assertGreater(len(log_calls), 0)
        
        # Since DEV=true, it should return early before committing
        commit_calls = [call for call in mock_syscmd.call_args_list 
                       if len(call[0]) > 0 and 'commit --allow-empty' in str(call[0][0])]
        self.assertEqual(len(commit_calls), 0)
    
    @patch('anilist_readme.git.syscmd')
    def test_git_check_activity_timezone_aware_comparison(self, mock_syscmd):
        """Test that timezone-aware datetime comparison works correctly"""
        # Mock git log to return ISO 8601 format with timezone
        test_date = datetime.now(timezone.utc) - timedelta(days=70)
        iso_date = test_date.isoformat()
        
        def syscmd_side_effect(cmd, *args, **kwargs):
            if 'log' in cmd and 'pretty=format' in cmd:
                return iso_date
            return 0
        
        mock_syscmd.side_effect = syscmd_side_effect
        
        # This should not raise a TypeError
        try:
            git_check_activity("token", "email@example.com", "username")
        except TypeError as e:
            if "can't compare offset-naive and offset-aware" in str(e):
                self.fail("Timezone comparison failed - still comparing naive and aware datetimes")
            raise


class TestGitConfig(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.original_dev = environ.get("DEV")
        self.original_repo = environ.get("GITHUB_REPOSITORY")
        environ["DEV"] = "true"  # Prevent actual git commands
    
    def tearDown(self):
        """Clean up test environment"""
        if self.original_dev is None:
            environ.pop("DEV", None)
        else:
            environ["DEV"] = self.original_dev
        if self.original_repo is None:
            environ.pop("GITHUB_REPOSITORY", None)
        else:
            environ["GITHUB_REPOSITORY"] = self.original_repo
    
    @patch('anilist_readme.git.syscmd')
    def test_git_config_skipped_in_dev_mode(self, mock_syscmd):
        """Test that git_config is skipped when DEV=true"""
        git_config("email@example.com", "username", "token")
        
        # Should not call syscmd when DEV=true
        mock_syscmd.assert_not_called()
    
    @patch('anilist_readme.git.syscmd')
    def test_git_config_called_when_not_in_dev_mode(self, mock_syscmd):
        """Test that git_config calls syscmd when DEV is not set"""
        environ.pop("DEV", None)
        environ["GITHUB_REPOSITORY"] = "test/repo"  # Required for git_config
        
        git_config("email@example.com", "username", "token")
        
        # Should call syscmd 3 times (email, name, remote)
        self.assertEqual(mock_syscmd.call_count, 3)


class TestGitAddCommitPush(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.original_dev = environ.get("DEV")
        environ["DEV"] = "true"  # Prevent actual git commands
    
    def tearDown(self):
        """Clean up test environment"""
        if self.original_dev is None:
            environ.pop("DEV", None)
        else:
            environ["DEV"] = self.original_dev
    
    @patch('anilist_readme.git.syscmd')
    @patch('anilist_readme.git.git_config')
    def test_git_add_commit_push_skipped_in_dev_mode(self, mock_git_config, mock_syscmd):
        """Test that git_add_commit_push is skipped when DEV=true"""
        git_add_commit_push("README.md", "test message", "token", "email@example.com", "username")
        
        # Should not call syscmd when DEV=true
        add_calls = [call for call in mock_syscmd.call_args_list 
                    if len(call[0]) > 0 and 'git add' in str(call[0][0])]
        self.assertEqual(len(add_calls), 0)

