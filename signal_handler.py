# signal_handler.py

import signal
import sys
import time
import logging

# ============================
# Logger Configuration
# ============================

def setup_logger():
    """
    Sets up a logger to capture signal handling logs.

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
# Signal Handler Functions
# ============================

def handle_sigint(signum, frame):
    """
    Handles the SIGINT signal (Ctrl+C).

    Args:
        signum (int): Signal number.
        frame (frame): Current stack frame.
    """
    logger.info("SIGINT received. Exiting gracefully...")
    sys.exit(0)

def handle_sigterm(signum, frame):
    """
    Handles the SIGTERM signal (termination request).

    Args:
        signum (int): Signal number.
        frame (frame): Current stack frame.
    """
    logger.info("SIGTERM received. Exiting gracefully...")
    sys.exit(0)

# ============================
# Main Program Logic
# ============================

if __name__ == "__main__":
    # Set up logger
    logger = setup_logger()

    # Register signal handlers
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    logger.info("Signal handlers are set up. Press Ctrl+C to exit.")

    # Simulate a long-running process
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # This block is not strictly necessary since SIGINT is handled above,
        # but it's included here to demonstrate handling KeyboardInterrupt.
        logger.info("KeyboardInterrupt caught. Exiting...")
        sys.exit(0)