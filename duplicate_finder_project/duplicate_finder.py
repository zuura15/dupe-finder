import logging
import pytz
from collections import defaultdict
import argparse
from datetime import datetime
from file_utils import find_files, get_file_hash, load_hashes

# Define a custom logging formatter to use PST timezone
class PSTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        pst = pytz.timezone('America/Los_Angeles')
        record.created = datetime.fromtimestamp(record.created, pst)
        return super().formatTime(record, datefmt)

# Configure logging with PST timezone
logging.basicConfig(filename='duplicate_finder.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().handlers[0].setFormatter(PSTFormatter('%Y-%m-%d %H:%M:%S'))

# Supported video and image file extensions
VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.m4v', '.wmv', '.flv', '.mpeg', '.mpg']
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic']

def check_for_duplicates(files, existing_hashes):
    """Check for duplicate files and return a list of duplicate pairs."""
    logging.debug("Checking for duplicates")
    hash_map = defaultdict(list)
    duplicates = []

    for file_path in files:
        file_hash = get_file_hash(file_path, existing_hashes)

        if file_hash:
            hash_map[file_hash].append(file_path)

    for file_list in hash_map.values():
        if len(file_list) > 1:
            for file in file_list:
                for duplicate in file_list:
                    if file != duplicate:
                        logging.debug(f"Duplicate found: {file} <--> {duplicate}")
                        duplicates.append((file, duplicate))
    return duplicates

def main():
    parser = argparse.ArgumentParser(description="Duplicate Finder")
    parser.add_argument('directory1', help="First directory to check")
    parser.add_argument('directory2', nargs='?', help="Second directory to check (optional)")
    args = parser.parse_args()

    logging.info(f"Starting duplicate check for directories: {args.directory1}, {args.directory2}")

    # Load existing hashes
    existing_hashes = load_hashes()

    # Find all files in the specified directories
    all_files = find_files(args.directory1, VIDEO_EXTENSIONS + IMAGE_EXTENSIONS)
    if args.directory2:
        all_files.extend(find_files(args.directory2, VIDEO_EXTENSIONS + IMAGE_EXTENSIONS))

    # Check for duplicates
    duplicates = check_for_duplicates(all_files, existing_hashes)

    if duplicates:
        print("Duplicates found:")
        for file1, file2 in duplicates:
            print(f"{file1} <--> {file2}")
            logging.info(f"Duplicate found: {file1} <--> {file2}")
    else:
        print("No duplicates found.")
        logging.info("No duplicates found.")

if __name__ == "__main__":
    main()
