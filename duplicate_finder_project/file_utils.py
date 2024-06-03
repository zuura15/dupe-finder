import os
from pathlib import Path
import logging
from hash_utils import calculate_hash

def find_files(directory, extensions):
    """Find all files in a directory with the given extensions."""
    logging.debug(f"Finding files in directory: {directory} with extensions: {extensions}")
    files = []
    for ext in extensions:
        files.extend(Path(directory).rglob(f'*{ext}'))
    logging.debug(f"Found files: {files}")
    return files

def store_hash(file_path, file_hash):
    """Store a single file hash in a persistent storage."""
    logging.debug(f"Storing hash for file: {file_path}")
    try:
        with open('file_hashes.txt', 'a') as f:
            f.write(f"{file_path}:{file_hash}\n")
    except Exception as e:
        logging.error(f"Error storing hash for {file_path}: {e}")

def load_hashes():
    """Load file hashes from persistent storage."""
    logging.debug("Loading file hashes from storage")
    hash_map = {}
    try:
        if os.path.exists('file_hashes.txt'):
            with open('file_hashes.txt', 'r') as f:
                for line in f:
                    file_path, file_hash = line.strip().split(':')
                    hash_map[file_path] = file_hash
    except Exception as e:
        logging.error(f"Error loading hashes: {e}")
    logging.debug(f"Loaded hashes: {hash_map}")
    return hash_map

def get_file_hash(file_path, existing_hashes):
    """Get the hash of a file, calculating and storing it if necessary."""
    file_path_str = str(file_path)
    if file_path_str in existing_hashes:
        logging.debug(f"Using cached hash for file: {file_path}")
        return existing_hashes[file_path_str]
    else:
        logging.debug(f"Calculating new hash for file: {file_path}")
        file_hash = calculate_hash(file_path_str)
        if file_hash:
            store_hash(file_path_str, file_hash)
            existing_hashes[file_path_str] = file_hash
        return file_hash
