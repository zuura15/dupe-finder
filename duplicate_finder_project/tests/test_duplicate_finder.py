import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import argparse
import duplicate_finder

class TestDuplicateFinder(unittest.TestCase):

    @patch("duplicate_finder.find_files", return_value=[Path("file1.mp4"), Path("file2.mp4")])
    @patch("duplicate_finder.get_file_hash", side_effect=["hash1", "hash2"])
    def test_check_for_duplicates_no_duplicates(self, mock_get_file_hash, mock_find_files):
        files = [Path("file1.mp4"), Path("file2.mp4")]
        existing_hashes = {}
        result = duplicate_finder.check_for_duplicates(files, existing_hashes)
        self.assertListEqual(result, [])

    @patch("duplicate_finder.find_files", return_value=[Path("file1.mp4"), Path("file2.mp4")])
    @patch("duplicate_finder.get_file_hash", side_effect=["hash1", "hash1"])
    def test_check_for_duplicates_with_duplicates(self, mock_get_file_hash, mock_find_files):
        files = [Path("file1.mp4"), Path("file2.mp4")]
        existing_hashes = {}
        result = duplicate_finder.check_for_duplicates(files, existing_hashes)
        self.assertListEqual(result, [("file1.mp4", "file2.mp4"), ("file2.mp4", "file1.mp4")])

    @patch("duplicate_finder.find_files")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(directory1="dir1", directory2="dir2"))
    def test_main(self, mock_parse_args, mock_find_files):
        with patch('builtins.print') as mocked_print:
            mock_find_files.side_effect = [
                [Path("dir1/file1.mp4"), Path("dir1/file2.mp4")],
                [Path("dir2/file3.mp4"), Path("dir2/file4.mp4")]
            ]
            duplicate_finder.main()
            mocked_print.assert_any_call("No duplicates found.")

if __name__ == "__main__":
    unittest.main()
