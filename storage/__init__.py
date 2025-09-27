
from typing import Any, Dict, List, Optional, Union

# storage/__init__.py

"""
Storage Utilities for Framework0.

This module provides functions to handle various data storage operations,
including reading from and writing to different storage systems. It aims to
standardize data storage across Framework0, ensuring consistency and reusability.

Features:
- `read_from_storage`: Reads data from a specified storage system.
- `write_to_storage`: Writes data to a specified storage system.
"""

from .local_storage import read_from_local, write_to_local
from .cloud_storage import read_from_cloud, write_to_cloud
from .database_storage import read_from_database, write_to_database

__all__ = [
    "read_from_local",
    "write_to_local",
    "read_from_cloud",
    "write_to_cloud",
    "read_from_database",
    "write_to_database",
]
