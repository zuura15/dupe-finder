import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from pathlib import Path
import file_utils

class TestFileUtils(unittest.TestCase):

    @patch("file_utils.Path.rglob")
    def test_find_files(self, mock_rglob):
        mock_rglob.return_value = [Path("dummy1.mp4"), Path("dummy2.jpg")]
        result = file_utils.find_files("dummy_dir", [".mp4", ".jpg"])
        self.assertListEqual(result, [Path("dummy1.mp4"), Path("dummy2.jpg")])

    @patch("builtins.open", new_callable=mock_open)
    def test_store_hash(self, mock_file):
        file_path = "file1"
        file_hash = "hash1"
        file_utils.store_hash(file_path, file_hash)
        mock_file().write.assert_called_once_with("file1:hash1\n")

    @patch("builtins.open", new_callable=mock_open, read_data="file1:hash1\nfile2:hash2\n")
    def test_load_hashes(self, mock_file):
        expected_result = {"file1": "hash1", "file2": "hash2"}
        result = file_utils.load_hashes()
        self.assertDictEqual(result, expected_result)

    @patch("os.path.exists", return_value=False)
    def test_load_hashes_file_not_exist(self, mock_exists):
        result = file_utils.load_hashes()
        self.assertDictEqual(result, {})

    @patch("file_utils.calculate_hash", return_value="hash1")
    @patch("file_utils.store_hash")
    def test_get_file_hash_new_hash(self, mock_store_hash, mock_calculate_hash):
        existing_hashes = {}
        file_path = Path("file1")
        result = file_utils.get_file_hash(file_path, existing_hashes)
        self.assertEqual(result, "hash1")
        self.assertIn("file1", existing_hashes)
        mock_store_hash.assert_called_once_with("file1", "hash1")

    @patch("file_utils.calculate_hash")
    @patch("file_utils.store_hash")
    def test_get_file_hash_existing_hash(self, mock_store_hash, mock_calculate_hash):
        existing_hashes = {"file1": "hash1"}
        file_path = Path("file1")
        result = file_utils.get_file_hash(file_path, existing_hashes)
        self.assertEqual(result, "hash1")
        mock_calculate_hash.assert_not_called()
        mock_store_hash.assert_not_called()
