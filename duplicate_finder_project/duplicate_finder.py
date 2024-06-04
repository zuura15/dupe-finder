import logging
import pytz
from collections import defaultdict
import argparse
from datetime import datetime
from file_utils import find_files, get_file_hash, load_hashes
import pytz
from datetime import datetime

# Define a custom logging formatter to use PST timezone
class PSTFormatter(logging.Formatter):
    converter = pytz.timezone('America/Los_Angeles').localize

    def formatTime(self, record, datefmt=None):
        dt = self.converter(datetime.fromtimestamp(record.created))
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

# Configure logging with PST timezone
logging.basicConfig(filename='duplicate_finder.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
#logging.getLogger().handlers[0].setFormatter(PSTFormatter("%Y-%m-%d %H:%M:%S"))

# Add console handler
# Add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logging.getLogger().addHandler(console_handler)

# Supported video and image file extensions
VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.m4v', '.wmv', '.flv', '.mpeg', '.mpg']
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic']

def check_for_duplicates(files, existing_hashes):
    """Check for duplicate files and return a list of duplicate pairs."""
    logging.debug("Checking for duplicates")
    hash_map = defaultdict(list)
    duplicates = []

    total_files = len(files)
    logging.debug(f"Total files to process: {total_files}")

    for i, file_path in enumerate(files, start=1):
        logging.debug(f"Processing file {i} of {total_files}: {file_path}")
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
