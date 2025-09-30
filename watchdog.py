# watchdog.py

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ============================
# Logger Configuration
# ============================

def setup_logger() -> logging.Logger:
    """
    Sets up a logger to capture filesystem event logs.

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
# Event Handler Class
# ============================

class EventHandler(FileSystemEventHandler):
    """
    Custom event handler that processes filesystem events.
    """
    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        Args:
            event (FileSystemEvent): The event that triggered this method.
        """
        if event.is_directory:
            return  # Ignore directory modifications
        logger.info(f"File modified: {event.src_path}")

    def on_created(self, event):
        """
        Called when a file or directory is created.

        Args:
            event (FileSystemEvent): The event that triggered this method.
        """
        if event.is_directory:
            return  # Ignore directory creations
        logger.info(f"File created: {event.src_path}")

    def on_deleted(self, event):
        """
        Called when a file or directory is deleted.

        Args:
            event (FileSystemEvent): The event that triggered this method.
        """
        if event.is_directory:
            return  # Ignore directory deletions
        logger.info(f"File deleted: {event.src_path}")

# ============================
# Main Function
# ============================

def main(path: str):
    """
    Main function to set up and start the watchdog observer.

    Args:
        path (str): The directory path to monitor.
    """
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    logger.info(f"Monitoring started on {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Monitoring stopped")
    observer.join()

# ============================
# Entry Point
# ============================

if __name__ == "__main__":
    # Set up logger
    logger = setup_logger()

    # Determine the directory to monitor
    directory_to_watch = sys.argv[1] if len(sys.argv) > 1 else '.'

    # Start monitoring
    main(directory_to_watch)