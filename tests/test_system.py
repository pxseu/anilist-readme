import unittest
from unittest.mock import patch, MagicMock
from anilist_readme.system import syscmd


class TestSyscmd(unittest.TestCase):
    @patch('anilist_readme.system.run')
    def test_syscmd_pipes_to_terminal_by_default(self, mock_run):
        """Test that syscmd pipes to terminal by default (capture_output=False)"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = syscmd("echo hello")
        
        mock_run.assert_called_once_with("echo hello", shell=True, stderr=-2)
        self.assertEqual(result, 0)
    
    @patch('anilist_readme.system.Popen')
    def test_syscmd_captures_output(self, mock_popen):
        """Test that syscmd captures output when capture_output=True"""
        mock_process = MagicMock()
        mock_process.wait.return_value = None
        mock_process.stdout.read.return_value = b"test output"
        mock_popen.return_value = mock_process
        
        result = syscmd("echo test", capture_output=True)
        
        mock_popen.assert_called_once()
        self.assertEqual(result, b"test output")
    
    @patch('anilist_readme.system.Popen')
    def test_syscmd_captures_output_with_encoding(self, mock_popen):
        """Test that syscmd decodes output when encoding is provided"""
        mock_process = MagicMock()
        mock_process.wait.return_value = None
        mock_process.stdout.read.return_value = b"test output"
        mock_popen.return_value = mock_process
        
        result = syscmd("echo test", capture_output=True, encoding='utf-8')
        
        self.assertEqual(result, "test output")
    
    @patch('anilist_readme.system.Popen')
    def test_syscmd_returns_returncode_when_no_output(self, mock_popen):
        """Test that syscmd returns returncode when output is empty"""
        mock_process = MagicMock()
        mock_process.wait.return_value = None
        mock_process.stdout.read.return_value = b""
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        
        result = syscmd("false", capture_output=True)
        
        self.assertEqual(result, 1)

