import unittest
from unittest.mock import patch, MagicMock
from os import environ
from anilist_readme.actions_utils import actions_input, add_secret, escape_data


class TestActionsInput(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Save original environment variables
        self.original_env = {}
        for key in list(environ.keys()):
            if key.startswith("INPUT_"):
                self.original_env[key] = environ[key]
                del environ[key]
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove test environment variables
        for key in list(environ.keys()):
            if key.startswith("INPUT_"):
                del environ[key]
        # Restore original environment variables
        for key, value in self.original_env.items():
            environ[key] = value
    
    def test_actions_input_returns_value_when_set(self):
        """Test that actions_input returns the value when environment variable is set"""
        environ["INPUT_TEST_VALUE"] = "test123"
        
        result = actions_input("TEST_VALUE", optional=True)
        
        self.assertEqual(result, "test123")
    
    def test_actions_input_returns_none_when_optional_and_not_set(self):
        """Test that actions_input returns None when optional=True and value not set"""
        result = actions_input("MISSING_VALUE", optional=True)
        
        self.assertIsNone(result)
    
    def test_actions_input_raises_when_required_and_not_set(self):
        """Test that actions_input raises ValueError when optional=False and value not set"""
        with self.assertRaises(ValueError) as context:
            actions_input("MISSING_VALUE", optional=False)
        
        self.assertIn("MISSING_VALUE is required", str(context.exception))
    
    def test_actions_input_converts_spaces_to_underscores(self):
        """Test that actions_input converts spaces to underscores in the key"""
        environ["INPUT_TEST_VALUE"] = "test123"
        
        result = actions_input("TEST VALUE", optional=True)
        
        self.assertEqual(result, "test123")
    
    def test_actions_input_uppercases_key(self):
        """Test that actions_input uppercases the key"""
        environ["INPUT_TEST_VALUE"] = "test123"
        
        result = actions_input("test_value", optional=True)
        
        self.assertEqual(result, "test123")
    
    @patch('anilist_readme.actions_utils.add_secret')
    def test_actions_input_masks_secret_values(self, mock_add_secret):
        """Test that actions_input masks secret values (GH_TOKEN, COMMIT_EMAIL, COMMIT_USERNAME)"""
        environ["INPUT_GH_TOKEN"] = "secret_token_123"
        
        actions_input("GH_TOKEN", optional=True)
        
        mock_add_secret.assert_called_once_with("secret_token_123")
    
    @patch('anilist_readme.actions_utils.add_secret')
    def test_actions_input_masks_commit_email(self, mock_add_secret):
        """Test that actions_input masks COMMIT_EMAIL"""
        environ["INPUT_COMMIT_EMAIL"] = "test@example.com"
        
        actions_input("COMMIT_EMAIL", optional=True)
        
        mock_add_secret.assert_called_once_with("test@example.com")
    
    @patch('anilist_readme.actions_utils.add_secret')
    def test_actions_input_masks_commit_username(self, mock_add_secret):
        """Test that actions_input masks COMMIT_USERNAME"""
        environ["INPUT_COMMIT_USERNAME"] = "testuser"
        
        actions_input("COMMIT_USERNAME", optional=True)
        
        mock_add_secret.assert_called_once_with("testuser")
    
    @patch('anilist_readme.actions_utils.add_secret')
    def test_actions_input_does_not_mask_non_secret_values(self, mock_add_secret):
        """Test that actions_input does not mask non-secret values"""
        environ["INPUT_USER_ID"] = "12345"
        
        actions_input("USER_ID", optional=True)
        
        mock_add_secret.assert_not_called()
    
    @patch('anilist_readme.actions_utils.add_secret')
    def test_actions_input_does_not_mask_when_value_is_none(self, mock_add_secret):
        """Test that actions_input does not mask when value is None"""
        actions_input("GH_TOKEN", optional=True)
        
        mock_add_secret.assert_not_called()


class TestAddSecret(unittest.TestCase):
    @patch('builtins.print')
    @patch('anilist_readme.actions_utils.escape_data')
    @patch('anilist_readme.actions_utils.CMD_STR', '::')
    def test_add_secret_calls_escape_data(self, mock_escape_data, mock_print):
        """Test that add_secret calls escape_data on the secret"""
        mock_escape_data.return_value = "escaped_secret"
        
        add_secret("test_secret")
        
        mock_escape_data.assert_called_once_with("test_secret")
        mock_print.assert_called_once_with("::add-mask::escaped_secret")
    
    @patch('builtins.print')
    @patch('anilist_readme.actions_utils.CMD_STR', '::')
    def test_add_secret_formats_output_correctly(self, mock_print):
        """Test that add_secret formats output with CMD_STR"""
        with patch('anilist_readme.actions_utils.escape_data', return_value="escaped"):
            add_secret("test")
            
            mock_print.assert_called_once_with("::add-mask::escaped")


class TestEscapeData(unittest.TestCase):
    def test_escape_data_json_encodes_string(self):
        """Test that escape_data JSON encodes the string"""
        result = escape_data("test")
        
        self.assertEqual(result, '"test"')
    
    def test_escape_data_escapes_percent_sign(self):
        """Test that escape_data escapes percent signs"""
        result = escape_data("test%value")
        
        self.assertEqual(result, '"test%25value"')
    
    def test_escape_data_escapes_newlines(self):
        """Test that escape_data JSON encodes newlines"""
        result = escape_data("line1\nline2")
        
        # json.dumps escapes newlines as \\n, then replace looks for \n (actual newline)
        # Since json.dumps already escaped it, the replace doesn't match
        # So we get the JSON-escaped version
        self.assertEqual(result, '"line1\\nline2"')
    
    def test_escape_data_escapes_carriage_returns(self):
        """Test that escape_data JSON encodes carriage returns"""
        result = escape_data("line1\rline2")
        
        # json.dumps escapes carriage returns as \\r
        self.assertEqual(result, '"line1\\rline2"')
    
    def test_escape_data_escapes_multiple_special_chars(self):
        """Test that escape_data handles multiple special characters"""
        result = escape_data("test%value\nwith\rnewlines")
        
        self.assertIn("%25", result)  # percent is replaced
        # Newlines and carriage returns are JSON-escaped by json.dumps
        self.assertIn("\\n", result)  # JSON-escaped newline
        self.assertIn("\\r", result)  # JSON-escaped carriage return
    
    def test_escape_data_handles_empty_string(self):
        """Test that escape_data handles empty strings"""
        result = escape_data("")
        
        self.assertEqual(result, '""')
    
    def test_escape_data_handles_special_json_characters(self):
        """Test that escape_data properly JSON encodes special characters"""
        result = escape_data('test"quote')
        
        # JSON encoding should escape the quote
        self.assertIn('\\"', result)
    
    def test_escape_data_handles_unicode(self):
        """Test that escape_data handles unicode characters"""
        result = escape_data("test🌸emoji")
        
        # Should be JSON encoded
        self.assertIsInstance(result, str)
        self.assertIn("test", result)

