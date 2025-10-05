#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test case for the Enhanced Persistence Framework.

This module provides a comprehensive test for the persistence framework,
demonstrating the capabilities of the delta compression, snapshot management,
caching, and integrated persistence features.
"""
import os
import time
import json
import tempfile
import unittest
from typing import Dict, Any, List

# Import the persistence modules
from orchestrator.persistence.core import StorageBackend, CacheStrategy, DeltaStrategy
from orchestrator.persistence.delta import DeltaCompressor
from orchestrator.persistence.snapshot import SnapshotManager
from orchestrator.persistence.cache import Cache, PersistentCache, TieredCache
from orchestrator.persistence.enhanced import EnhancedPersistenceV2, create_enhanced_persistence


class TestEnhancedPersistence(unittest.TestCase):
    """Test case for Enhanced Persistence functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        
        # Create an instance of EnhancedPersistenceV2
        self.persistence = EnhancedPersistenceV2(
            base_path=os.path.join(self.test_dir, "persistence"),
            storage_backend=StorageBackend.FILE_SYSTEM,
            cache_strategy=CacheStrategy.TIERED,
            delta_strategy=DeltaStrategy.AUTO,
            max_snapshots=5,
            enable_compression=True,
            thread_safe=True
        )
        
        # Sample test data
        self.test_data = {
            "user": {
                "name": "Test User",
                "email": "test@example.com",
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            },
            "app_state": {
                "last_opened": ["file1.txt", "file2.txt"],
                "window_position": [100, 200, 800, 600]
            },
            "metrics": {
                "visits": 42,
                "actions": 123,
                "conversion_rate": 0.28
            }
        }
    
    def tearDown(self):
        """Clean up after each test."""
        # Clean up persistence resources
        self.persistence.cleanup()
        
        # Remove temporary directory
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_basic_persistence(self):
        """Test basic save and load operations."""
        # Save data
        self.persistence.save(self.test_data)
        
        # Load data
        loaded_data = self.persistence.load()
        
        # Assert data was loaded correctly
        self.assertEqual(loaded_data, self.test_data)
    
    def test_key_operations(self):
        """Test individual key operations (get, set, delete)."""
        # Initialize with empty data
        self.persistence.save({})
        
        # Set individual keys
        self.persistence.set("key1", "value1")
        self.persistence.set("key2", {"nested": "value2"})
        
        # Get keys
        value1 = self.persistence.get("key1")
        value2 = self.persistence.get("key2")
        
        # Assert values were retrieved correctly
        self.assertEqual(value1, "value1")
        self.assertEqual(value2, {"nested": "value2"})
        
        # Delete a key
        deleted = self.persistence.delete("key1")
        
        # Assert key was deleted
        self.assertTrue(deleted)
        self.assertIsNone(self.persistence.get("key1"))
        
        # Delete non-existent key
        deleted = self.persistence.delete("non_existent")
        
        # Assert key was not deleted
        self.assertFalse(deleted)
    
    def test_snapshots(self):
        """Test snapshot creation and restoration."""
        # Save initial data
        self.persistence.save(self.test_data)
        
        # Create a snapshot
        snapshot1 = self.persistence.create_snapshot("initial", "Initial data")
        
        # Modify data
        modified_data = self.test_data.copy()
        modified_data["user"]["name"] = "Modified User"
        modified_data["metrics"]["visits"] = 50
        
        # Save modified data
        self.persistence.save(modified_data)
        
        # Create another snapshot
        snapshot2 = self.persistence.create_snapshot("modified", "Modified data")
        
        # Restore initial snapshot
        restored_data = self.persistence.restore_snapshot(snapshot1)
        
        # Assert data was restored correctly
        self.assertEqual(restored_data, self.test_data)
        
        # Restore modified snapshot
        restored_data = self.persistence.restore_snapshot(snapshot2)
        
        # Assert data was restored correctly
        self.assertEqual(restored_data, modified_data)
        
        # Test snapshot by tag
        restored_data = self.persistence.restore_snapshot_by_tag("initial")
        
        # Assert data was restored correctly
        self.assertEqual(restored_data, self.test_data)
    
    def test_delta_snapshots(self):
        """Test delta snapshot creation and restoration."""
        # Save initial data
        self.persistence.save(self.test_data)
        
        # Create a base snapshot
        base_snapshot = self.persistence.create_snapshot("base", "Base data")
        
        # Modify data slightly
        modified_data = self.test_data.copy()
        modified_data["user"]["name"] = "Modified User"
        
        # Save modified data
        self.persistence.save(modified_data)
        
        # Create a delta snapshot
        delta_snapshot = self.persistence.create_delta_snapshot(
            base_version=base_snapshot,
            tag="delta",
            description="Delta data"
        )
        
        # Restore delta snapshot
        restored_data = self.persistence.restore_snapshot(delta_snapshot)
        
        # Assert data was restored correctly
        self.assertEqual(restored_data, modified_data)
    
    def test_snapshot_comparison(self):
        """Test snapshot comparison functionality."""
        # Save initial data
        self.persistence.save(self.test_data)
        
        # Create a snapshot
        snapshot1 = self.persistence.create_snapshot("initial", "Initial data")
        
        # Modify data
        modified_data = self.test_data.copy()
        modified_data["user"]["name"] = "Modified User"
        
        # Save modified data
        self.persistence.save(modified_data)
        
        # Create another snapshot
        snapshot2 = self.persistence.create_snapshot("modified", "Modified data")
        
        # Compare snapshots
        comparison = self.persistence.compare_snapshots(snapshot1, snapshot2)
        
        # Assert comparison contains expected fields
        self.assertIn("version1", comparison)
        self.assertIn("version2", comparison)
        self.assertIn("delta_info", comparison)
        self.assertIn("is_different", comparison)
        
        # Assert snapshots are different
        self.assertTrue(comparison["is_different"])
    
    def test_import_export(self):
        """Test import and export functionality."""
        # Save data
        self.persistence.save(self.test_data)
        
        # Export data
        export_path = os.path.join(self.test_dir, "export.json")
        self.persistence.export_data(export_path)
        
        # Clear data
        self.persistence.clear()
        
        # Import data
        imported_data = self.persistence.import_data(export_path)
        
        # Assert data was imported correctly
        self.assertEqual(imported_data, self.test_data)
    
    def test_metrics(self):
        """Test metrics collection and reporting."""
        # Perform some operations to generate metrics
        self.persistence.save(self.test_data)
        self.persistence.load()
        self.persistence.get("user")
        self.persistence.create_snapshot()
        
        # Get metrics
        metrics = self.persistence.get_metrics()
        
        # Assert metrics contain expected fields
        self.assertIn("cache", metrics)
        self.assertIn("delta", metrics)
        self.assertIn("snapshot_count", metrics)
    
    def test_factory_function(self):
        """Test the persistence factory function."""
        # Create persistence using factory function
        persistence = create_enhanced_persistence(
            base_path=os.path.join(self.test_dir, "factory_persistence"),
            storage_backend=StorageBackend.FILE_SYSTEM,
            cache_strategy=CacheStrategy.MEMORY,
            delta_strategy=DeltaStrategy.DICT
        )
        
        # Test basic operations
        persistence.save(self.test_data)
        loaded_data = persistence.load()
        
        # Assert data was loaded correctly
        self.assertEqual(loaded_data, self.test_data)
        
        # Clean up
        persistence.cleanup()


if __name__ == "__main__":
    unittest.main()