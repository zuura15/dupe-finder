import unittest
from unittest.mock import patch, mock_open, MagicMock
import hash_utils
import hashlib

class TestHashUtils(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=b"test data")
    def test_calculate_hash(self, mock_file):
        file_path = "dummy_path"
        expected_hash = hashlib.md5(b"test data").hexdigest()
        result = hash_utils.calculate_hash(file_path)
        self.assertEqual(result, expected_hash)

    @patch("builtins.open", new_callable=mock_open, read_data=b"")
    def test_calculate_hash_empty_file(self, mock_file):
        file_path = "dummy_path"
        expected_hash = hashlib.md5(b"").hexdigest()
        result = hash_utils.calculate_hash(file_path)
        self.assertEqual(result, expected_hash)
