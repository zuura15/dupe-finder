import hashlib
import logging

def calculate_hash(file_path, block_size=65536):
    """Calculate and return the hash of a file."""
    logging.debug(f"Calculating hash for file: {file_path}")
    try:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buffer = file.read(block_size)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file.read(block_size)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating hash for {file_path}: {e}")
        return None
