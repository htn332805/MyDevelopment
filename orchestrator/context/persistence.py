# orchestrator/context/persistence.py
# This module implements the Persistence class, which handles controlled flushing
# of context data to disk or database in the IAF0 framework.
# It supports interval-based flushes (e.g., every 10 seconds), diff-only flushes
# (only changed keys), and on-demand flushes.
# Compression is applied using gzip for efficiency, especially for large contexts.
# The class integrates with the Context class for data access, MemoryBus for in-memory state,
# and version_control.py for versioning during persistence.
# It uses the storage/db_adapter.py for DB interactions and file I/O for disk storage.
# This minimizes disk I/O during active testing, flushing only as needed.

import gzip  # Imported for compression of data during flushing to reduce storage size.
import json  # Imported for serializing data to JSON format before flushing.
import os  # Imported for file system operations like checking paths and writing files.
import time  # Imported for handling interval-based flushing using timestamps.
from typing import Any, Dict, Optional  # Imported for type hints to improve code readability.
from orchestrator.context.context import Context  # Imported to access the Context class for data retrieval.
from storage.db_adapter import DBAdapter  # Imported for database interactions (MySQL/SQLite3).
from orchestrator.context.version_control import VersionControl  # Imported for versioning integration during flushes.

class Persistence:
    """
    Persistence class for flushing context data to disk or DB with compression.
    Supports interval, diff-only, and on-demand modes.
    Integrates with DBAdapter for persistent storage and VersionControl for versioning.
    """

    def __init__(self, context: Context, db_adapter: Optional[DBAdapter] = None, flush_interval: int = 10, flush_dir: str = "./persistence") -> None:
        # Initializes the Persistence instance.
        # Requires a Context object; optionally takes DBAdapter, flush interval (seconds), and disk directory.
        self.context = context  # Stores the reference to the Context object for data access.
        self.db_adapter = db_adapter  # Optional DBAdapter for database flushing; if None, only disk is used.
        self.flush_interval = flush_interval  # Interval in seconds for automatic flushes.
        self.flush_dir = flush_dir  # Directory path for disk-based flush files.
        self.last_flush_time = time.time()  # Tracks the timestamp of the last flush for interval checks.
        self.last_flushed_data: Dict[str, Any] = {}  # Stores the last flushed data for diff calculations.
        os.makedirs(self.flush_dir, exist_ok=True)  # Creates the flush directory if it doesn't exist, avoiding errors.

    def flush(self, mode: str = "full", compress: bool = True) -> None:
        # Performs a flush operation based on the mode.
        # Modes: 'full' (all data), 'diff' (only changes), 'demand' (forced full).
        # Args:
        #   mode: Flush mode ('full', 'diff', 'demand').
        #   compress: Whether to apply gzip compression.
        current_data = self.context.to_dict()  # Retrieves the current context data as a dict.
        data_to_flush = current_data if mode in ("full", "demand") else self._compute_diff(current_data)  # Determines data based on mode.
        flushed = False  # Flag to track if flush occurred.

        if self.db_adapter:  # Checks if a DBAdapter is provided.
            self._flush_to_db(data_to_flush, mode)  # Calls private method to flush to database.
            flushed = True  # Sets flag to indicate flush happened.

        self._flush_to_disk(data_to_flush, compress)  # Calls private method to flush to disk, regardless of DB.
        flushed = True  # Sets flag (redundant if DB flushed, but ensures).

        if flushed:  # If a flush occurred:
            self.last_flush_time = time.time()  # Updates the last flush timestamp.
            self.last_flushed_data = current_data.copy()  # Updates the last flushed data for future diffs.
            VersionControl(self.db_adapter).commit(self.context)  # Integrates with VersionControl to commit the version.

    def check_and_flush(self) -> None:
        # Checks if interval has passed and performs an interval-based flush if needed.
        # This can be called periodically by the framework (e.g., in a timer thread).
        current_time = time.time()  # Gets the current timestamp.
        if current_time - self.last_flush_time >= self.flush_interval:  # Checks if interval has elapsed.
            self.flush(mode="diff")  # Performs a diff-based flush.

    def load_from_disk(self, file_name: str) -> None:
        # Loads persisted data from disk into the context.
        # Handles decompression if applicable.
        # Args:
        #   file_name: Name of the file to load (relative to flush_dir).
        file_path = os.path.join(self.flush_dir, file_name)  # Constructs the full file path.
        if not os.path.exists(file_path):  # Checks if the file exists.
            raise FileNotFoundError(f"Persistence file not found: {file_path}")  # Raises error if missing.

        with open(file_path, 'rb') as f:  # Opens the file in binary read mode.
            content = f.read()  # Reads the entire file content.
            if file_path.endswith('.gz'):  # Checks if the file is gzipped.
                content = gzip.decompress(content)  # Decompresses if gzipped.
            data = json.loads(content)  # Deserializes the JSON content to a dict.

        for key, value in data.items():  # Iterates over the loaded data.
            self.context.set(key, value, who="persistence_load")  # Sets each key-value in the context with traceability.

    def load_from_db(self, version_id: Optional[str] = None) -> None:
        # Loads data from the database into the context.
        # Optionally loads a specific version.
        # Args:
        #   version_id: Optional version ID to load.
        if not self.db_adapter:  # Checks if DBAdapter is available.
            raise ValueError("No DBAdapter configured for loading.")  # Raises error if not.

        data = self.db_adapter.load_context(version_id)  # Calls DBAdapter to load the context data.
        for key, value in data.items():  # Iterates over the loaded data.
            self.context.set(key, value, who="db_load")  # Sets each key-value in the context.

    def _flush_to_disk(self, data: Dict[str, Any], compress: bool) -> None:
        # Private method to flush data to disk.
        # Serializes to JSON and optionally compresses with gzip.
        # Args:
        #   data: Dict of data to flush.
        #   compress: Whether to gzip the file.
        timestamp = int(time.time())  # Gets current timestamp for unique file naming.
        file_name = f"context_{timestamp}.json"  # Base file name.
        if compress:  # If compression is enabled:
            file_name += ".gz"  # Appends .gz extension.
        file_path = os.path.join(self.flush_dir, file_name)  # Constructs full path.

        json_data = json.dumps(data)  # Serializes the data to JSON string.
        content = json_data.encode('utf-8')  # Encodes to bytes for writing.
        if compress:  # If compression:
            content = gzip.compress(content)  # Compresses the bytes.

        with open(file_path, 'wb') as f:  # Opens file in binary write mode.
            f.write(content)  # Writes the (compressed) content to file.

    def _flush_to_db(self, data: Dict[str, Any], mode: str) -> None:
        # Private method to flush data to the database.
        # Uses DBAdapter to store.
        # Args:
        #   data: Dict to flush.
        #   mode: Flush mode for potential DB-specific handling.
        if not self.db_adapter:  # Redundant check, but ensures safety.
            return  # Early return if no adapter.
        self.db_adapter.save_context(data, mode)  # Calls DBAdapter's save method.

    def _compute_diff(self, current_data: Dict[str, Any]) -> Dict[str, Any]:
        # Private method to compute the diff between current and last flushed data.
        # Returns only changed or new keys.
        # Args:
        #   current_data: Current context dict.
        # Returns: Dict of differences.
        diff = {}  # Initializes empty diff dict.
        for key, value in current_data.items():  # Iterates over current data.
            if key not in self.last_flushed_data or self.last_flushed_data[key] != value:  # Checks for new or changed.
                diff[key] = value  # Adds to diff if different.
        return diff  # Returns the diff dict.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: Formatted string with config details.
        return f"Persistence(interval={self.flush_interval}, dir={self.flush_dir}, db={self.db_adapter is not None})"  # Summary string.

# No additional code outside the class; this module focuses on the Persistence class.
# In the framework, Persistence is instantiated with a Context and used by the runner or server
# to manage data persistence without heavy I/O during active sessions.