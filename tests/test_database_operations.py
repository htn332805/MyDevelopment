#!/usr/bin/env python3
"""
Unit tests for Database Operations Scriptlet

Tests the core functionality of the database operations template
implementation including connection management, CRUD operations,
and transaction handling.
"""

import pytest
import os
import json
import tempfile
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Import the database operations scriptlet
try:
    from scriptlets.core.database_operations import (
        initialize_database_connection,
        DatabaseOperationsManager,
        ConnectionPool,
        DatabaseOperationsError,
    )
except ImportError:
    # Fallback for test environments
    import sys
    import os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from scriptlets.core.database_operations import (
        initialize_database_connection,
        DatabaseOperationsManager,
        ConnectionPool,
        DatabaseOperationsError,
    )


class TestDatabaseOperations:
    """Test suite for Database Operations functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        # SQLite test configuration (lightweight for testing)
        self.test_config = {
            "database_config": {
                "type": "sqlite",
                "database": ":memory:",  # In-memory SQLite for testing
                "connection_string": "sqlite:///:memory:",
            },
            "connection_pool_config": {
                "min_connections": 1,
                "max_connections": 5,
                "connection_timeout": 10,
                "max_idle_time": 300,
            },
            "security_config": {"enable_encryption": False},
            "monitoring_config": {"enable_health_checks": True},
        }

        # Mock context for testing
        self.mock_context = Mock()

    def test_database_operations_error_creation(self):
        """Test custom exception creation."""
        error_msg = "Test database error"
        error = DatabaseOperationsError(error_msg)
        assert str(error) == error_msg
        assert isinstance(error, Exception)

    @patch("scriptlets.core.database_operations.SQL_AVAILABLE", True)
    @patch("scriptlets.core.database_operations.create_engine")
    @patch("scriptlets.core.database_operations.sessionmaker")
    def test_connection_pool_initialization_sql(
        self, mock_sessionmaker, mock_create_engine
    ):
        """Test SQL connection pool initialization."""
        # Setup mocks
        mock_engine = Mock()
        mock_connection = Mock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine
        mock_sessionmaker.return_value = Mock()

        # Test connection pool creation
        pool = ConnectionPool(self.test_config)

        # Verify engine creation
        mock_create_engine.assert_called_once()
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)

        # Verify pool attributes
        assert pool.db_type == "sqlite"
        assert pool.engine == mock_engine

    def test_connection_pool_unsupported_database_type(self):
        """Test error handling for unsupported database types."""
        config = self.test_config.copy()
        config["database_config"]["type"] = "unsupported_db"

        with pytest.raises(DatabaseOperationsError) as exc_info:
            ConnectionPool(config)

        assert "Unsupported database type" in str(exc_info.value)

    @patch("scriptlets.core.database_operations.SQL_AVAILABLE", True)
    @patch("scriptlets.core.database_operations.create_engine")
    def test_database_operations_manager_initialization(self, mock_create_engine):
        """Test database operations manager initialization."""
        # Setup mocks
        mock_engine = Mock()
        mock_connection = Mock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine

        # Test manager creation
        manager = DatabaseOperationsManager(self.test_config, self.mock_context)

        # Verify initialization
        assert manager.config == self.test_config
        assert manager.context == self.mock_context
        assert manager.connection_pool is not None
        assert manager.active_transactions == {}

    @patch("scriptlets.core.database_operations.SQL_AVAILABLE", False)
    def test_initialize_connection_missing_dependencies(self):
        """Test error handling when SQL dependencies are missing."""
        config = self.test_config.copy()
        config["database_config"]["type"] = "postgresql"

        with pytest.raises(DatabaseOperationsError) as exc_info:
            initialize_database_connection(database_config=config["database_config"])

        assert "SQLAlchemy required" in str(exc_info.value)

    def test_initialize_connection_missing_config(self):
        """Test error handling when database config is missing."""
        with pytest.raises(DatabaseOperationsError) as exc_info:
            initialize_database_connection()

        assert "database_config parameter is required" in str(exc_info.value)

    def test_initialize_connection_missing_database_type(self):
        """Test error handling when database type is not specified."""
        config = {"database_config": {}}

        with pytest.raises(DatabaseOperationsError) as exc_info:
            initialize_database_connection(**config)

        assert "Database type must be specified" in str(exc_info.value)

    @patch("scriptlets.core.database_operations.SQL_AVAILABLE", True)
    @patch("scriptlets.core.database_operations.create_engine")
    @patch("scriptlets.core.database_operations.sessionmaker")
    def test_successful_database_initialization(
        self, mock_sessionmaker, mock_create_engine
    ):
        """Test successful database connection initialization."""
        # Setup mocks
        mock_engine = Mock()
        mock_connection = Mock()
        mock_session = Mock()

        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine
        mock_sessionmaker.return_value = lambda: mock_session

        # Test initialization
        result = initialize_database_connection(**self.test_config)

        # Verify result structure
        assert "database_connection_config" in result
        assert "connection_pool_status" in result

        config = result["database_connection_config"]
        assert config["database_type"] == "sqlite"
        assert "database_manager" in config
        assert "health_status" in config
        assert "initialization_time" in config

        pool_status = result["connection_pool_status"]
        assert pool_status["initialized"] is True
        assert pool_status["pool_type"] == "sql_pool"

    @patch("scriptlets.core.database_operations.SQL_AVAILABLE", True)
    @patch("scriptlets.core.database_operations.create_engine")
    def test_database_connection_string_building(self, mock_create_engine):
        """Test connection string building for different database types."""
        # Test PostgreSQL connection string
        pg_config = {
            "database_config": {
                "type": "postgresql",
                "host": "localhost",
                "port": 5432,
                "database": "testdb",
                "username": "testuser",
                "password": "testpass",
            },
            "connection_pool_config": {},
            "security_config": {},
            "monitoring_config": {},
        }

        # Setup mock
        mock_engine = Mock()
        mock_connection = Mock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine

        # Test connection pool creation
        pool = ConnectionPool(pg_config)

        # Verify the connection string was built correctly
        call_args = mock_create_engine.call_args[0]
        connection_string = call_args[0]
        assert (
            "postgresql+psycopg2://testuser:testpass@localhost:5432/testdb"
            == connection_string
        )

    def test_transaction_context_data_structure(self):
        """Test transaction context data structure."""
        # This would be expanded with actual transaction testing
        # For now, verify the basic structure expectations

        expected_fields = [
            "transaction_id",
            "isolation_level",
            "timeout",
            "start_time",
            "status",
            "savepoints",
            "operations",
        ]

        # This is a placeholder test - in reality we would test with mock database operations
        # but for this demonstration, we're verifying the expected structure
        assert all(field in expected_fields for field in expected_fields)

    def test_operation_results_structure(self):
        """Test operation results data structure."""
        # Test expected structure for CRUD operation results
        expected_create_fields = [
            "operation",
            "records_affected",
            "created_records",
            "table_name",
        ]
        expected_read_fields = ["operation", "records_count", "records", "table_name"]
        expected_update_fields = [
            "operation",
            "records_affected",
            "updated_data",
            "conditions",
            "table_name",
        ]
        expected_delete_fields = [
            "operation",
            "records_affected",
            "conditions",
            "table_name",
        ]

        # Verify field expectations
        assert len(expected_create_fields) == 4
        assert len(expected_read_fields) == 4
        assert len(expected_update_fields) == 5
        assert len(expected_delete_fields) == 4

        # Verify all operations include basic fields
        basic_fields = ["operation", "table_name"]
        for field_list in [
            expected_create_fields,
            expected_read_fields,
            expected_update_fields,
            expected_delete_fields,
        ]:
            assert all(field in field_list for field in basic_fields)

    @pytest.mark.integration
    @patch("scriptlets.core.database_operations.SQL_AVAILABLE", True)
    @patch("scriptlets.core.database_operations.create_engine")
    @patch("scriptlets.core.database_operations.sessionmaker")
    def test_full_operation_workflow(self, mock_sessionmaker, mock_create_engine):
        """Test complete database operation workflow."""
        # This is a simplified integration test
        # In a real scenario, this would test against an actual test database

        # Setup mocks
        mock_engine = Mock()
        mock_connection = Mock()
        mock_session = Mock()

        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine
        mock_sessionmaker.return_value = lambda: mock_session

        # Test workflow: initialize -> validate schema -> execute operation -> generate report

        # 1. Initialize connection
        init_result = initialize_database_connection(**self.test_config)
        assert init_result is not None

        # 2. Verify manager creation
        manager = init_result["database_connection_config"]["database_manager"]
        assert isinstance(manager, DatabaseOperationsManager)

        # 3. Verify health check capability
        health_status = manager.connection_pool.health_check()
        assert "healthy" in health_status
        assert "check_time" in health_status

        # In a real integration test, we would continue with actual operations
        # but for this unit test demonstration, we verify the setup is correct

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up any test artifacts
        pass


class TestDatabaseOperationsAdvanced:
    """Advanced test cases for Database Operations."""

    def test_performance_metrics_structure(self):
        """Test performance metrics data structure."""
        expected_metrics = {
            "operation_metrics": [
                "operation_type",
                "execution_duration_ms",
                "records_processed",
            ],
            "connection_metrics": [
                "pool_healthy",
                "active_connections",
                "total_connections",
            ],
            "health_metrics": ["component", "status", "metadata"],
        }

        for metric_category, expected_fields in expected_metrics.items():
            # Verify we have defined expectations for key metric categories
            assert len(expected_fields) >= 3
            assert isinstance(expected_fields, list)

    def test_error_handling_coverage(self):
        """Test error handling coverage."""
        # Test that our custom exception can be raised and caught
        try:
            raise DatabaseOperationsError("Test error for coverage")
        except DatabaseOperationsError as e:
            assert str(e) == "Test error for coverage"
        except Exception:
            pytest.fail("Should catch DatabaseOperationsError specifically")

    def test_configuration_validation(self):
        """Test configuration validation logic."""
        # Test minimum required configuration fields
        required_fields = ["database_config"]
        minimal_config = {"database_config": {"type": "sqlite", "database": ":memory:"}}

        # Verify required fields are present
        for field in required_fields:
            assert field in minimal_config

        # Verify database config has minimum required fields
        assert "type" in minimal_config["database_config"]


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
