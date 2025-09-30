# cleanup.py

import os
import time
import argparse
import logging
from pathlib import Path

# ============================
# Logger Configuration
# ============================

def setup_logger():
    """
    Sets up a logger to capture cleanup logs.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Console handler for logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# ============================
# File Cleanup Function
# ============================

def cleanup_old_files(directory, days, dry_run, force):
    """
    Removes files and empty directories older than a specified number of days.

    Args:
        directory (str): The directory to clean up.
        days (int): The age of the files in days.
        dry_run (bool): If True, only logs the actions without performing them.
        force (bool): If True, deletes files without asking for confirmation.
    """
    logger = setup_logger()
    cutoff_time = time.time() - (days * 86400)  # Convert days to seconds

    # Convert to Path object for easier manipulation
    directory_path = Path(directory)

    if not directory_path.exists():
        logger.error(f"Directory {directory} does not exist.")
        return

    if not directory_path.is_dir():
        logger.error(f"{directory} is not a valid directory.")
        return

    logger.info(f"Starting cleanup in {directory} for files older than {days} days.")

    # Walk through the directory
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_path = Path(root) / name
            try:
                # Check if the file is older than the cutoff time
                if file_path.stat().st_mtime < cutoff_time:
                    if dry_run:
                        logger.info(f"Dry run: {file_path} would be deleted.")
                    else:
                        if force or input(f"Delete {file_path}? (y/n): ").lower() == 'y':
                            os.remove(file_path)
                            logger.info(f"Deleted file: {file_path}")
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")

        # Remove empty directories
        for name in dirs:
            dir_path = Path(root) / name
            try:
                if not os.listdir(dir_path):  # Directory is empty
                    if dry_run:
                        logger.info(f"Dry run: {dir_path} would be removed.")
                    else:
                        if force or input(f"Remove empty directory {dir_path}? (y/n): ").lower() == 'y':
                            os.rmdir(dir_path)
                            logger.info(f"Removed empty directory: {dir_path}")
            except Exception as e:
                logger.error(f"Error processing directory {dir_path}: {e}")

    logger.info("Cleanup completed.")

# ============================
# Main Function
# ============================

def main():
    """
    Main function to parse arguments and initiate the cleanup process.
    """
    parser = argparse.ArgumentParser(description="Clean up old files and empty directories.")
    parser.add_argument('directory', help="Directory to clean up.")
    parser.add_argument('-d', '--days', type=int, default=30, help="Age of files to delete in days.")
    parser.add_argument('-D', '--dryrun', action='store_true', help="Perform a dry run without deleting anything.")
    parser.add_argument('-f', '--force', action='store_true', help="Force deletion without confirmation.")
    args = parser.parse_args()

    cleanup_old_files(args.directory, args.days, args.dryrun, args.force)

# ============================
# Entry Point
# ============================

if __name__ == "__main__":
    main()