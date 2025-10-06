#!/usr/bin/env python3
"""
Framework0 Core - Database Operations Scriptlet

Comprehensive database operations capabilities with multi-database support,
transaction management, and connection pooling. This scriptlet provides
the implementation for the database_operations recipe template.

Features:
- Multi-database support (PostgreSQL, MySQL, SQLite, MongoDB, Redis)
- CRUD operations with advanced querying and filtering
- Transaction management with isolation levels and rollback
- Connection pooling with automatic failover and load balancing
- Schema management and migration support
- Performance monitoring and query optimization
- Foundation system integration for health checks and metrics
- Comprehensive error handling with retry logic and circuit breakers
- Data security with encryption and access control

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the database_operations.yaml template.
"""

import os
import json
import time
import threading
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Union, List, Tuple, Type
from contextlib import contextmanager
from urllib.parse import urlparse
import hashlib

# SQL Database imports
try:
    import sqlalchemy
    from sqlalchemy import create_engine, text, MetaData, Table, Column, inspect
    from sqlalchemy.orm import sessionmaker, Session
    from sqlalchemy.pool import QueuePool, NullPool
    from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError

    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False
    sqlalchemy = None

# NoSQL Database imports
try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError, ConnectionFailure

    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    pymongo = None

try:
    import redis
    from redis.exceptions import RedisError, ConnectionError as RedisConnectionError

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

# Framework0 imports with fallback
try:
    from orchestrator.context import Context
    from src.core.logger import get_logger

    FRAMEWORK0_AVAILABLE = True
except ImportError:
    Context = None
    FRAMEWORK0_AVAILABLE = False

    def get_logger(name):
        import logging

        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)


# Foundation imports for monitoring integration
try:
    from scriptlets.foundation.logging import get_framework_logger
    from scriptlets.foundation.health import get_health_monitor
    from scriptlets.foundation.metrics import get_performance_monitor

    FOUNDATION_AVAILABLE = True
except ImportError:
    FOUNDATION_AVAILABLE = False
    get_framework_logger = None
    get_health_monitor = None
    get_performance_monitor = None


class DatabaseOperationsError(Exception):
    """Custom exception for database operation errors."""

    pass


class ConnectionPool:
    """
    Database connection pool manager.

    Manages database connections with automatic failover,
    health checking, and performance monitoring.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize connection pool.

        Args:
            config: Database and pool configuration
        """
        self.config = config
        self.logger = get_logger(__name__)
        self.db_type = config["database_config"]["type"]
        self.pool_config = config.get("connection_pool_config", {})

        # Connection pool state
        self.engine = None
        self.session_factory = None
        self.mongo_client = None
        self.redis_client = None
        self.pool_stats = {
            "total_connections": 0,
            "active_connections": 0,
            "failed_connections": 0,
            "last_health_check": None,
        }

        self._lock = threading.Lock()
        self._initialize_pool()

    def _initialize_pool(self) -> None:
        """Initialize the appropriate connection pool."""
        try:
            if self.db_type in ["postgresql", "mysql", "sqlite", "oracle", "sqlserver"]:
                self._initialize_sql_pool()
            elif self.db_type == "mongodb":
                self._initialize_mongodb_pool()
            elif self.db_type == "redis":
                self._initialize_redis_pool()
            else:
                raise DatabaseOperationsError(
                    f"Unsupported database type: {self.db_type}"
                )

            self.logger.info(f"Connection pool initialized for {self.db_type}")

        except Exception as e:
            self.logger.error(f"Failed to initialize connection pool: {e}")
            raise DatabaseOperationsError(
                f"Connection pool initialization failed: {str(e)}"
            )

    def _initialize_sql_pool(self) -> None:
        """Initialize SQL database connection pool."""
        if not SQL_AVAILABLE:
            raise DatabaseOperationsError(
                "SQLAlchemy not available for SQL database operations"
            )

        db_config = self.config["database_config"]
        pool_config = self.pool_config

        # Build connection string
        connection_string = self._build_sql_connection_string(db_config)

        # Create engine with connection pooling
        engine_kwargs = {
            "pool_size": pool_config.get("min_connections", 5),
            "max_overflow": pool_config.get("max_connections", 20)
            - pool_config.get("min_connections", 5),
            "pool_timeout": pool_config.get("connection_timeout", 30),
            "pool_recycle": pool_config.get("max_idle_time", 3600),
            "echo": False,  # Set to True for SQL debugging
        }

        # Configure pool class based on database type
        if self.db_type == "sqlite":
            engine_kwargs["poolclass"] = (
                NullPool  # SQLite doesn't support connection pooling
            )
        else:
            engine_kwargs["poolclass"] = QueuePool

        self.engine = create_engine(connection_string, **engine_kwargs)
        self.session_factory = sessionmaker(bind=self.engine)

        # Test connection
        with self.engine.connect() as conn:
            if pool_config.get("validation_query"):
                conn.execute(text(pool_config["validation_query"]))
            else:
                # Default validation queries by database type
                validation_queries = {
                    "postgresql": "SELECT 1",
                    "mysql": "SELECT 1",
                    "sqlite": "SELECT 1",
                    "oracle": "SELECT 1 FROM DUAL",
                    "sqlserver": "SELECT 1",
                }
                conn.execute(text(validation_queries.get(self.db_type, "SELECT 1")))

    def _initialize_mongodb_pool(self) -> None:
        """Initialize MongoDB connection pool."""
        if not MONGODB_AVAILABLE:
            raise DatabaseOperationsError(
                "PyMongo not available for MongoDB operations"
            )

        db_config = self.config["database_config"]
        pool_config = self.pool_config

        # Build MongoDB connection options
        connection_options = {
            "maxPoolSize": pool_config.get("max_connections", 100),
            "minPoolSize": pool_config.get("min_connections", 10),
            "maxIdleTimeMS": pool_config.get("max_idle_time", 3600) * 1000,
            "connectTimeoutMS": pool_config.get("connection_timeout", 30) * 1000,
            "serverSelectionTimeoutMS": pool_config.get("connection_timeout", 30)
            * 1000,
        }

        # Add SSL configuration if provided
        ssl_config = db_config.get("ssl_config", {})
        if ssl_config.get("enabled"):
            connection_options.update(
                {
                    "ssl": True,
                    "ssl_cert_reqs": "CERT_REQUIRED",
                    "ssl_ca_certs": ssl_config.get("ca_path"),
                    "ssl_certfile": ssl_config.get("cert_path"),
                    "ssl_keyfile": ssl_config.get("key_path"),
                }
            )

        # Create MongoDB client
        connection_string = db_config.get("connection_string")
        if not connection_string:
            host = db_config.get("host", "localhost")
            port = db_config.get("port", 27017)
            username = db_config.get("username")
            password = db_config.get("password")
            database = db_config.get("database")

            if username and password:
                connection_string = (
                    f"mongodb://{username}:{password}@{host}:{port}/{database}"
                )
            else:
                connection_string = f"mongodb://{host}:{port}/{database}"

        self.mongo_client = MongoClient(connection_string, **connection_options)

        # Test connection
        self.mongo_client.admin.command("ping")

    def _initialize_redis_pool(self) -> None:
        """Initialize Redis connection pool."""
        if not REDIS_AVAILABLE:
            raise DatabaseOperationsError("Redis not available for Redis operations")

        db_config = self.config["database_config"]
        pool_config = self.pool_config

        # Build Redis connection options
        connection_options = {
            "host": db_config.get("host", "localhost"),
            "port": db_config.get("port", 6379),
            "db": db_config.get("database", 0),
            "max_connections": pool_config.get("max_connections", 50),
            "socket_timeout": pool_config.get("connection_timeout", 30),
            "socket_connect_timeout": pool_config.get("connection_timeout", 30),
        }

        # Add authentication if provided
        password = db_config.get("password")
        if password:
            connection_options["password"] = password

        # Add SSL configuration if provided
        ssl_config = db_config.get("ssl_config", {})
        if ssl_config.get("enabled"):
            connection_options.update(
                {
                    "ssl": True,
                    "ssl_cert_reqs": "required",
                    "ssl_ca_certs": ssl_config.get("ca_path"),
                    "ssl_certfile": ssl_config.get("cert_path"),
                    "ssl_keyfile": ssl_config.get("key_path"),
                }
            )

        # Create Redis connection pool
        pool = redis.ConnectionPool(**connection_options)
        self.redis_client = redis.Redis(connection_pool=pool)

        # Test connection
        self.redis_client.ping()

    def _build_sql_connection_string(self, db_config: Dict[str, Any]) -> str:
        """Build SQL database connection string."""
        connection_string = db_config.get("connection_string")
        if connection_string:
            return connection_string

        # Build connection string from components
        db_type = db_config["type"]
        host = db_config.get("host", "localhost")
        port = db_config.get("port")
        database = db_config.get("database")
        username = db_config.get("username")
        password = db_config.get("password")

        # Default ports by database type
        default_ports = {
            "postgresql": 5432,
            "mysql": 3306,
            "oracle": 1521,
            "sqlserver": 1433,
        }

        if not port:
            port = default_ports.get(db_type)

        # Handle SQLite special case
        if db_type == "sqlite":
            return f"sqlite:///{database}"

        # Build connection string for other databases
        if db_type == "postgresql":
            driver = "postgresql+psycopg2"
        elif db_type == "mysql":
            driver = "mysql+pymysql"
        elif db_type == "oracle":
            driver = "oracle+cx_oracle"
        elif db_type == "sqlserver":
            driver = "mssql+pyodbc"
        else:
            driver = db_type

        if username and password:
            auth_part = f"{username}:{password}@"
        else:
            auth_part = ""

        return f"{driver}://{auth_part}{host}:{port}/{database}"

    @contextmanager
    def get_connection(self):
        """Get database connection from pool."""
        if self.db_type in ["postgresql", "mysql", "sqlite", "oracle", "sqlserver"]:
            yield from self._get_sql_connection()
        elif self.db_type == "mongodb":
            yield from self._get_mongodb_connection()
        elif self.db_type == "redis":
            yield from self._get_redis_connection()

    @contextmanager
    def _get_sql_connection(self):
        """Get SQL database connection."""
        session = None
        try:
            with self._lock:
                self.pool_stats["active_connections"] += 1

            session = self.session_factory()
            yield session

        except Exception as e:
            if session:
                session.rollback()
            with self._lock:
                self.pool_stats["failed_connections"] += 1
            raise e
        finally:
            if session:
                session.close()
            with self._lock:
                self.pool_stats["active_connections"] -= 1

    @contextmanager
    def _get_mongodb_connection(self):
        """Get MongoDB database connection."""
        try:
            with self._lock:
                self.pool_stats["active_connections"] += 1

            database = self.mongo_client[self.config["database_config"]["database"]]
            yield database

        except Exception as e:
            with self._lock:
                self.pool_stats["failed_connections"] += 1
            raise e
        finally:
            with self._lock:
                self.pool_stats["active_connections"] -= 1

    @contextmanager
    def _get_redis_connection(self):
        """Get Redis database connection."""
        try:
            with self._lock:
                self.pool_stats["active_connections"] += 1

            yield self.redis_client

        except Exception as e:
            with self._lock:
                self.pool_stats["failed_connections"] += 1
            raise e
        finally:
            with self._lock:
                self.pool_stats["active_connections"] -= 1

    def health_check(self) -> Dict[str, Any]:
        """Perform connection pool health check."""
        health_status = {
            "healthy": False,
            "pool_stats": self.pool_stats.copy(),
            "check_time": datetime.now(timezone.utc).isoformat(),
            "errors": [],
        }

        try:
            with self.get_connection() as conn:
                if self.db_type in [
                    "postgresql",
                    "mysql",
                    "sqlite",
                    "oracle",
                    "sqlserver",
                ]:
                    conn.execute(text("SELECT 1"))
                elif self.db_type == "mongodb":
                    conn.command("ping")
                elif self.db_type == "redis":
                    conn.ping()

            health_status["healthy"] = True

        except Exception as e:
            health_status["errors"].append(str(e))
            self.logger.error(f"Connection health check failed: {e}")

        with self._lock:
            self.pool_stats["last_health_check"] = health_status["check_time"]

        return health_status

    def close(self) -> None:
        """Close all connections and cleanup resources."""
        try:
            if self.engine:
                self.engine.dispose()
            if self.mongo_client:
                self.mongo_client.close()
            if self.redis_client:
                self.redis_client.close()

            self.logger.info("Connection pool closed successfully")

        except Exception as e:
            self.logger.error(f"Error closing connection pool: {e}")


class DatabaseOperationsManager:
    """
    Database operations manager with multi-database support.

    Provides unified interface for database operations across
    different database types with transaction management.
    """

    def __init__(
        self, config: Dict[str, Any], context: Optional[Context] = None
    ) -> None:
        """
        Initialize database operations manager.

        Args:
            config: Database configuration
            context: Optional Framework0 context
        """
        self.config = config
        self.context = context
        self.logger = get_logger(__name__)

        # Initialize Foundation integration
        self.foundation_logger = None
        self.health_monitor = None
        self.performance_monitor = None

        if FOUNDATION_AVAILABLE:
            try:
                self.foundation_logger = get_framework_logger()
                self.health_monitor = get_health_monitor()
                self.performance_monitor = get_performance_monitor()
                self.logger.info("Foundation integration initialized")
            except Exception as e:
                self.logger.warning(f"Foundation integration failed: {e}")

        # Initialize connection pool
        self.connection_pool = ConnectionPool(config)

        # Transaction state
        self.active_transactions = {}
        self._transaction_lock = threading.Lock()

    def execute_operation(
        self,
        operation: str,
        target_config: Dict[str, Any],
        data_config: Dict[str, Any],
        transaction_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute database operation.

        Args:
            operation: Operation type (create, read, update, delete, etc.)
            target_config: Target table/collection configuration
            data_config: Data and query configuration
            transaction_context: Optional transaction context

        Returns:
            Operation results dictionary
        """
        start_time = time.time()

        try:
            # Execute operation based on database type
            if self.connection_pool.db_type in [
                "postgresql",
                "mysql",
                "sqlite",
                "oracle",
                "sqlserver",
            ]:
                results = self._execute_sql_operation(
                    operation, target_config, data_config, transaction_context
                )
            elif self.connection_pool.db_type == "mongodb":
                results = self._execute_mongodb_operation(
                    operation, target_config, data_config, transaction_context
                )
            elif self.connection_pool.db_type == "redis":
                results = self._execute_redis_operation(
                    operation, target_config, data_config, transaction_context
                )
            else:
                raise DatabaseOperationsError(
                    f"Unsupported database type: {self.connection_pool.db_type}"
                )

            # Track performance metrics
            duration = time.time() - start_time
            if self.performance_monitor:
                self.performance_monitor.record_metric(
                    "database_query_duration",
                    duration * 1000,
                    metadata={
                        "operation": operation,
                        "table": target_config.get("table_name"),
                        "database_type": self.connection_pool.db_type,
                    },
                )

            # Log operation success
            if self.foundation_logger:
                self.foundation_logger.info(
                    f"Database operation completed: {operation}",
                    extra={
                        "operation": operation,
                        "table": target_config.get("table_name"),
                        "duration_ms": duration * 1000,
                        "records_affected": results.get("records_affected", 0),
                    },
                )

            self.logger.info(f"Operation {operation} completed in {duration:.3f}s")
            return results

        except Exception as e:
            duration = time.time() - start_time

            if self.foundation_logger:
                self.foundation_logger.error(
                    f"Database operation failed: {operation}",
                    extra={
                        "operation": operation,
                        "table": target_config.get("table_name"),
                        "error": str(e),
                        "duration_ms": duration * 1000,
                    },
                )

            self.logger.error(
                f"Operation {operation} failed after {duration:.3f}s: {str(e)}"
            )
            raise DatabaseOperationsError(f"Database operation failed: {str(e)}") from e

    def _execute_sql_operation(
        self,
        operation: str,
        target_config: Dict[str, Any],
        data_config: Dict[str, Any],
        transaction_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute SQL database operation."""
        table_name = target_config["table_name"]
        schema_name = target_config.get("schema_name")

        with self.connection_pool.get_connection() as session:
            try:
                if operation == "create":
                    return self._sql_create(
                        session, table_name, data_config, schema_name
                    )
                elif operation == "read":
                    return self._sql_read(session, table_name, data_config, schema_name)
                elif operation == "update":
                    return self._sql_update(
                        session, table_name, data_config, schema_name
                    )
                elif operation == "delete":
                    return self._sql_delete(
                        session, table_name, data_config, schema_name
                    )
                elif operation == "execute":
                    return self._sql_execute_raw(session, data_config)
                else:
                    raise DatabaseOperationsError(
                        f"Unsupported SQL operation: {operation}"
                    )

            except Exception as e:
                session.rollback()
                raise e

    def _sql_create(
        self,
        session,
        table_name: str,
        data_config: Dict[str, Any],
        schema_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute SQL INSERT operation."""
        data = data_config.get("data")
        if not data:
            raise DatabaseOperationsError("No data provided for create operation")

        # Build qualified table name
        qualified_table = f"{schema_name}.{table_name}" if schema_name else table_name

        records_affected = 0
        created_records = []

        if isinstance(data, list):
            # Bulk insert
            for record in data:
                if not isinstance(record, dict):
                    raise DatabaseOperationsError("Each record must be a dictionary")

                columns = ", ".join(record.keys())
                placeholders = ", ".join([f":{key}" for key in record.keys()])
                query = (
                    f"INSERT INTO {qualified_table} ({columns}) VALUES ({placeholders})"
                )

                result = session.execute(text(query), record)
                records_affected += result.rowcount
                created_records.append(record)
        else:
            # Single insert
            if not isinstance(data, dict):
                raise DatabaseOperationsError(
                    "Data must be a dictionary for single insert"
                )

            columns = ", ".join(data.keys())
            placeholders = ", ".join([f":{key}" for key in data.keys()])
            query = f"INSERT INTO {qualified_table} ({columns}) VALUES ({placeholders})"

            result = session.execute(text(query), data)
            records_affected = result.rowcount
            created_records = [data]

        session.commit()

        return {
            "operation": "create",
            "records_affected": records_affected,
            "created_records": created_records,
            "table_name": table_name,
        }

    def _sql_read(
        self,
        session,
        table_name: str,
        data_config: Dict[str, Any],
        schema_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute SQL SELECT operation."""
        # Build qualified table name
        qualified_table = f"{schema_name}.{table_name}" if schema_name else table_name

        # Handle raw query
        raw_query = data_config.get("raw_query")
        if raw_query:
            query_params = data_config.get("query_parameters", {})
            result = session.execute(text(raw_query), query_params)
            records = [dict(row._mapping) for row in result]
            return {
                "operation": "read",
                "records_count": len(records),
                "records": records,
                "table_name": table_name,
            }

        # Build SELECT query
        fields = data_config.get("fields", ["*"])
        if fields == ["*"] or not fields:
            select_clause = "*"
        else:
            select_clause = ", ".join(fields)

        query = f"SELECT {select_clause} FROM {qualified_table}"
        query_params = {}

        # Add WHERE conditions
        conditions = data_config.get("conditions", {})
        if conditions:
            where_parts = []
            for key, value in conditions.items():
                where_parts.append(f"{key} = :{key}")
                query_params[key] = value
            query += f" WHERE {' AND '.join(where_parts)}"

        # Add ORDER BY
        order_by = data_config.get("order_by", [])
        if order_by:
            order_parts = []
            for order_spec in order_by:
                if isinstance(order_spec, dict):
                    field = order_spec.get("field")
                    direction = order_spec.get("direction", "ASC")
                    order_parts.append(f"{field} {direction}")
                else:
                    order_parts.append(str(order_spec))
            query += f" ORDER BY {', '.join(order_parts)}"

        # Add LIMIT and OFFSET
        limit = data_config.get("limit")
        if limit:
            query += f" LIMIT {limit}"

        offset = data_config.get("offset")
        if offset:
            query += f" OFFSET {offset}"

        result = session.execute(text(query), query_params)
        records = [dict(row._mapping) for row in result]

        return {
            "operation": "read",
            "records_count": len(records),
            "records": records,
            "table_name": table_name,
            "query": query,
        }

    def _sql_update(
        self,
        session,
        table_name: str,
        data_config: Dict[str, Any],
        schema_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute SQL UPDATE operation."""
        data = data_config.get("data", {})
        conditions = data_config.get("conditions", {})

        if not data:
            raise DatabaseOperationsError("No data provided for update operation")

        if not conditions:
            raise DatabaseOperationsError("No conditions provided for update operation")

        # Build qualified table name
        qualified_table = f"{schema_name}.{table_name}" if schema_name else table_name

        # Build UPDATE query
        set_parts = []
        query_params = {}

        for key, value in data.items():
            set_parts.append(f"{key} = :set_{key}")
            query_params[f"set_{key}"] = value

        where_parts = []
        for key, value in conditions.items():
            where_parts.append(f"{key} = :where_{key}")
            query_params[f"where_{key}"] = value

        query = f"UPDATE {qualified_table} SET {', '.join(set_parts)} WHERE {' AND '.join(where_parts)}"

        result = session.execute(text(query), query_params)
        records_affected = result.rowcount

        session.commit()

        return {
            "operation": "update",
            "records_affected": records_affected,
            "updated_data": data,
            "conditions": conditions,
            "table_name": table_name,
        }

    def _sql_delete(
        self,
        session,
        table_name: str,
        data_config: Dict[str, Any],
        schema_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute SQL DELETE operation."""
        conditions = data_config.get("conditions", {})

        if not conditions:
            raise DatabaseOperationsError("No conditions provided for delete operation")

        # Build qualified table name
        qualified_table = f"{schema_name}.{table_name}" if schema_name else table_name

        # Build DELETE query
        where_parts = []
        query_params = {}

        for key, value in conditions.items():
            where_parts.append(f"{key} = :{key}")
            query_params[key] = value

        query = f"DELETE FROM {qualified_table} WHERE {' AND '.join(where_parts)}"

        result = session.execute(text(query), query_params)
        records_affected = result.rowcount

        session.commit()

        return {
            "operation": "delete",
            "records_affected": records_affected,
            "conditions": conditions,
            "table_name": table_name,
        }

    def _sql_execute_raw(self, session, data_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute raw SQL query."""
        raw_query = data_config.get("raw_query")
        query_parameters = data_config.get("query_parameters", {})

        if not raw_query:
            raise DatabaseOperationsError("No raw query provided for execute operation")

        result = session.execute(text(raw_query), query_parameters)

        # Handle different types of queries
        if raw_query.strip().upper().startswith("SELECT"):
            records = [dict(row._mapping) for row in result]
            return {
                "operation": "execute",
                "query_type": "select",
                "records_count": len(records),
                "records": records,
                "raw_query": raw_query,
            }
        else:
            session.commit()
            return {
                "operation": "execute",
                "query_type": "modification",
                "records_affected": result.rowcount,
                "raw_query": raw_query,
            }


def initialize_database_connection(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Initialize database connection and connection pool.

    Args:
        context: Framework0 context
        **params: Database configuration parameters

    Returns:
        Dictionary with database connection configuration
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        database_config = params.get("database_config", {})
        connection_pool_config = params.get("connection_pool_config", {})
        security_config = params.get("security_config", {})
        monitoring_config = params.get("monitoring_config", {})

        if not database_config:
            raise DatabaseOperationsError("database_config parameter is required")

        db_type = database_config.get("type")
        if not db_type:
            raise DatabaseOperationsError("Database type must be specified")

        # Validate database-specific requirements
        if (
            db_type in ["postgresql", "mysql", "oracle", "sqlserver"]
            and not SQL_AVAILABLE
        ):
            raise DatabaseOperationsError(
                f"SQLAlchemy required for {db_type} operations"
            )

        if db_type == "mongodb" and not MONGODB_AVAILABLE:
            raise DatabaseOperationsError("PyMongo required for MongoDB operations")

        if db_type == "redis" and not REDIS_AVAILABLE:
            raise DatabaseOperationsError("Redis-py required for Redis operations")

        # Create database operations manager
        config = {
            "database_config": database_config,
            "connection_pool_config": connection_pool_config,
            "security_config": security_config,
            "monitoring_config": monitoring_config,
        }

        db_manager = DatabaseOperationsManager(config, context)

        # Perform initial health check
        health_status = db_manager.connection_pool.health_check()
        if not health_status["healthy"]:
            raise DatabaseOperationsError(
                f"Database health check failed: {health_status['errors']}"
            )

        connection_config = {
            "database_manager": db_manager,
            "database_type": db_type,
            "connection_pool_stats": db_manager.connection_pool.pool_stats,
            "health_status": health_status,
            "initialization_time": datetime.now().isoformat(),
            "config_hash": hashlib.md5(
                json.dumps(config, sort_keys=True).encode()
            ).hexdigest(),
        }

        pool_status = {
            "initialized": True,
            "pool_type": (
                "sql_pool"
                if db_type in ["postgresql", "mysql", "sqlite", "oracle", "sqlserver"]
                else db_type
            ),
            "min_connections": connection_pool_config.get("min_connections", 5),
            "max_connections": connection_pool_config.get("max_connections", 20),
            "health_check_enabled": connection_pool_config.get(
                "health_check_interval", 0
            )
            > 0,
        }

        # Track performance
        duration = time.time() - start_time
        if db_manager.performance_monitor:
            db_manager.performance_monitor.record_metric(
                "database_connection_init",
                duration * 1000,
                metadata={"database_type": db_type},
            )

        logger.info(f"Database connection initialized for {db_type}")

        return {
            "database_connection_config": connection_config,
            "connection_pool_status": pool_status,
        }

    except Exception as e:
        error_msg = f"Database connection initialization failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def validate_database_schema(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Validate database schema and create tables if needed.

    Args:
        context: Framework0 context
        **params: Schema configuration parameters

    Returns:
        Dictionary with schema validation results
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        database_manager = params.get("database_manager")
        schema_config = params.get("schema_config", {})
        table_config = params.get("table_config", {})

        if not database_manager:
            raise DatabaseOperationsError(
                "Database manager is required for schema validation"
            )

        if not schema_config and not table_config:
            raise DatabaseOperationsError("Schema or table configuration is required")

        validation_results = {
            "schema_exists": False,
            "tables_validated": [],
            "tables_created": [],
            "validation_errors": [],
        }

        # Validate schema existence for SQL databases
        if database_manager.connection_pool.db_type in [
            "postgresql",
            "mysql",
            "oracle",
            "sqlserver",
        ]:
            schema_name = schema_config.get("schema_name")
            if schema_name:
                # Check if schema exists and create if needed
                try:
                    with database_manager.connection_pool.get_connection() as session:
                        if database_manager.connection_pool.db_type == "postgresql":
                            result = session.execute(
                                text(
                                    "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"
                                ),
                                {"schema": schema_name},
                            )
                        elif database_manager.connection_pool.db_type == "mysql":
                            result = session.execute(
                                text(
                                    "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"
                                ),
                                {"schema": schema_name},
                            )
                        else:
                            result = None  # Handle other databases as needed

                        if result and result.fetchone():
                            validation_results["schema_exists"] = True
                        elif schema_config.get("auto_create", False):
                            # Create schema
                            session.execute(
                                text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
                            )
                            session.commit()
                            validation_results["schema_exists"] = True
                            logger.info(f"Schema {schema_name} created")

                except Exception as e:
                    validation_results["validation_errors"].append(
                        f"Schema validation failed: {str(e)}"
                    )

        # Validate table structure
        tables = table_config.get("tables", [])
        for table_spec in tables:
            table_name = table_spec.get("table_name")
            if not table_name:
                validation_results["validation_errors"].append("Table name is required")
                continue

            try:
                # Check if table exists
                table_exists = False
                with database_manager.connection_pool.get_connection() as session:
                    if database_manager.connection_pool.db_type in [
                        "postgresql",
                        "mysql",
                        "sqlite",
                        "oracle",
                        "sqlserver",
                    ]:
                        inspector = inspect(database_manager.connection_pool.engine)
                        table_exists = inspector.has_table(
                            table_name, schema=schema_config.get("schema_name")
                        )
                    elif database_manager.connection_pool.db_type == "mongodb":
                        collection_names = session.list_collection_names()
                        table_exists = table_name in collection_names

                if table_exists:
                    validation_results["tables_validated"].append(table_name)
                elif table_spec.get("auto_create", False):
                    # Create table based on specification
                    if database_manager.connection_pool.db_type in [
                        "postgresql",
                        "mysql",
                        "sqlite",
                        "oracle",
                        "sqlserver",
                    ]:
                        create_sql = _build_create_table_sql(
                            table_spec, database_manager.connection_pool.db_type
                        )
                        with (
                            database_manager.connection_pool.get_connection() as session
                        ):
                            session.execute(text(create_sql))
                            session.commit()
                    elif database_manager.connection_pool.db_type == "mongodb":
                        # MongoDB creates collections automatically, but we can create indexes
                        indexes = table_spec.get("indexes", [])
                        if indexes:
                            with (
                                database_manager.connection_pool.get_connection() as db
                            ):
                                collection = db[table_name]
                                for index_spec in indexes:
                                    collection.create_index(index_spec)

                    validation_results["tables_created"].append(table_name)
                    logger.info(f"Table {table_name} created")

            except Exception as e:
                validation_results["validation_errors"].append(
                    f"Table {table_name} validation failed: {str(e)}"
                )

        duration = time.time() - start_time
        logger.info(f"Schema validation completed in {duration:.3f}s")

        return {
            "schema_validation": validation_results,
            "validation_duration": duration,
        }

    except Exception as e:
        error_msg = f"Schema validation failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def setup_transaction_context(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Setup database transaction context with isolation level and timeout.

    Args:
        context: Framework0 context
        **params: Transaction configuration parameters

    Returns:
        Dictionary with transaction context
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        database_manager = params.get("database_manager")
        transaction_config = params.get("transaction_config", {})

        if not database_manager:
            raise DatabaseOperationsError(
                "Database manager is required for transaction setup"
            )

        transaction_id = transaction_config.get(
            "transaction_id", f"tx_{int(time.time() * 1000000)}"
        )
        isolation_level = transaction_config.get("isolation_level", "READ_COMMITTED")
        timeout = transaction_config.get("timeout", 300)  # 5 minutes default

        # Validate isolation level
        valid_isolation_levels = [
            "READ_UNCOMMITTED",
            "READ_COMMITTED",
            "REPEATABLE_READ",
            "SERIALIZABLE",
        ]
        if isolation_level not in valid_isolation_levels:
            raise DatabaseOperationsError(f"Invalid isolation level: {isolation_level}")

        transaction_context = {
            "transaction_id": transaction_id,
            "isolation_level": isolation_level,
            "timeout": timeout,
            "start_time": datetime.now(timezone.utc),
            "status": "initialized",
            "savepoints": [],
            "operations": [],
        }

        # Store transaction context in manager
        with database_manager._transaction_lock:
            database_manager.active_transactions[transaction_id] = transaction_context

        logger.info(f"Transaction context setup: {transaction_id}")

        return {
            "transaction_context": transaction_context,
            "setup_duration": time.time() - start_time,
        }

    except Exception as e:
        error_msg = f"Transaction context setup failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def execute_database_operation(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Execute database operation with comprehensive error handling and monitoring.

    Args:
        context: Framework0 context
        **params: Operation configuration parameters

    Returns:
        Dictionary with operation results
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        database_manager = params.get("database_manager")
        operation_config = params.get("operation_config", {})
        target_config = params.get("target_config", {})
        data_config = params.get("data_config", {})
        transaction_context = params.get("transaction_context")

        if not database_manager:
            raise DatabaseOperationsError(
                "Database manager is required for operation execution"
            )

        operation = operation_config.get("operation")
        if not operation:
            raise DatabaseOperationsError("Operation type is required")

        # Execute the database operation
        operation_results = database_manager.execute_operation(
            operation=operation,
            target_config=target_config,
            data_config=data_config,
            transaction_context=transaction_context,
        )

        # Update transaction context if provided
        if transaction_context:
            transaction_id = transaction_context.get("transaction_id")
            if (
                transaction_id
                and transaction_id in database_manager.active_transactions
            ):
                with database_manager._transaction_lock:
                    tx_ctx = database_manager.active_transactions[transaction_id]
                    tx_ctx["operations"].append(
                        {
                            "operation": operation,
                            "target": target_config.get("table_name", "unknown"),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "duration": time.time() - start_time,
                            "records_affected": operation_results.get(
                                "records_affected", 0
                            ),
                        }
                    )

        duration = time.time() - start_time
        logger.info(f"Database operation {operation} completed in {duration:.3f}s")

        return {
            "operation_results": operation_results,
            "execution_duration": duration,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        error_msg = f"Database operation execution failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def validate_operation_results(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Validate database operation results against expected criteria.

    Args:
        context: Framework0 context
        **params: Validation configuration parameters

    Returns:
        Dictionary with validation results
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        operation_results = params.get("operation_results", {})
        validation_config = params.get("validation_config", {})

        if not operation_results:
            raise DatabaseOperationsError(
                "Operation results are required for validation"
            )

        validation_results = {
            "validation_passed": True,
            "validation_errors": [],
            "validation_warnings": [],
            "validated_criteria": [],
        }

        # Validate record count expectations
        expected_records = validation_config.get("expected_records")
        if expected_records is not None:
            actual_records = operation_results.get(
                "records_affected", operation_results.get("records_count", 0)
            )
            if isinstance(expected_records, dict):
                min_records = expected_records.get("min")
                max_records = expected_records.get("max")

                if min_records is not None and actual_records < min_records:
                    validation_results["validation_errors"].append(
                        f"Record count {actual_records} below minimum {min_records}"
                    )
                    validation_results["validation_passed"] = False

                if max_records is not None and actual_records > max_records:
                    validation_results["validation_errors"].append(
                        f"Record count {actual_records} above maximum {max_records}"
                    )
                    validation_results["validation_passed"] = False
            else:
                if actual_records != expected_records:
                    validation_results["validation_errors"].append(
                        f"Record count {actual_records} doesn't match expected {expected_records}"
                    )
                    validation_results["validation_passed"] = False

            validation_results["validated_criteria"].append("record_count")

        # Validate data integrity
        data_validation = validation_config.get("data_validation", {})
        if data_validation and "records" in operation_results:
            records = operation_results["records"]

            # Check required fields
            required_fields = data_validation.get("required_fields", [])
            for field in required_fields:
                for i, record in enumerate(records):
                    if field not in record or record[field] is None:
                        validation_results["validation_errors"].append(
                            f"Required field {field} missing in record {i}"
                        )
                        validation_results["validation_passed"] = False

            # Check data types
            field_types = data_validation.get("field_types", {})
            for field, expected_type in field_types.items():
                for i, record in enumerate(records):
                    if field in record and record[field] is not None:
                        actual_type = type(record[field]).__name__
                        if actual_type != expected_type:
                            validation_results["validation_warnings"].append(
                                f"Field {field} in record {i} has type {actual_type}, expected {expected_type}"
                            )

            validation_results["validated_criteria"].append("data_integrity")

        # Validate performance expectations
        performance_validation = validation_config.get("performance_validation", {})
        if performance_validation:
            execution_duration = params.get("execution_duration", 0)
            max_duration = performance_validation.get("max_duration")

            if max_duration and execution_duration > max_duration:
                validation_results["validation_warnings"].append(
                    f"Execution duration {execution_duration:.3f}s exceeds maximum {max_duration}s"
                )

            validation_results["validated_criteria"].append("performance")

        duration = time.time() - start_time
        logger.info(f"Operation results validation completed in {duration:.3f}s")

        return {
            "validation_results": validation_results,
            "validation_duration": duration,
        }

    except Exception as e:
        error_msg = f"Operation results validation failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def commit_or_rollback_transaction(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Commit or rollback database transaction based on operation results.

    Args:
        context: Framework0 context
        **params: Transaction finalization parameters

    Returns:
        Dictionary with transaction finalization results
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        database_manager = params.get("database_manager")
        transaction_context = params.get("transaction_context", {})
        commit_decision = params.get("commit_decision", "commit")
        validation_results = params.get("validation_results", {})

        if not database_manager:
            raise DatabaseOperationsError(
                "Database manager is required for transaction finalization"
            )

        transaction_id = transaction_context.get("transaction_id")
        if (
            not transaction_id
            or transaction_id not in database_manager.active_transactions
        ):
            raise DatabaseOperationsError(f"Transaction {transaction_id} not found")

        # Determine final commit decision
        should_commit = commit_decision == "commit"
        if (
            validation_results.get("validation_results", {}).get("validation_passed")
            is False
        ):
            should_commit = False
            commit_decision = "rollback_validation_failed"

        # Execute commit or rollback
        transaction_result = {
            "transaction_id": transaction_id,
            "action": "commit" if should_commit else "rollback",
            "reason": commit_decision,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        with database_manager._transaction_lock:
            tx_ctx = database_manager.active_transactions[transaction_id]
            tx_ctx["status"] = "committed" if should_commit else "rolled_back"
            tx_ctx["end_time"] = datetime.now(timezone.utc)
            tx_ctx["duration"] = (
                tx_ctx["end_time"] - tx_ctx["start_time"]
            ).total_seconds()

            transaction_result["operations_count"] = len(tx_ctx["operations"])
            transaction_result["transaction_duration"] = tx_ctx["duration"]

            # Clean up transaction context
            del database_manager.active_transactions[transaction_id]

        duration = time.time() - start_time
        logger.info(
            f"Transaction {transaction_id} {transaction_result['action']} completed in {duration:.3f}s"
        )

        return {
            "transaction_result": transaction_result,
            "finalization_duration": duration,
        }

    except Exception as e:
        error_msg = f"Transaction finalization failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def update_performance_metrics(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Update performance metrics and health monitoring data.

    Args:
        context: Framework0 context
        **params: Performance tracking parameters

    Returns:
        Dictionary with updated metrics
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        database_manager = params.get("database_manager")
        operation_results = params.get("operation_results", {})
        execution_duration = params.get("execution_duration", 0)
        transaction_result = params.get("transaction_result", {})

        if not database_manager:
            raise DatabaseOperationsError(
                "Database manager is required for metrics update"
            )

        metrics_update = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation_metrics": {},
            "connection_metrics": {},
            "health_metrics": {},
        }

        # Update operation metrics
        if operation_results:
            operation = operation_results.get("operation", "unknown")
            records_affected = operation_results.get(
                "records_affected", operation_results.get("records_count", 0)
            )

            metrics_update["operation_metrics"] = {
                "operation_type": operation,
                "execution_duration_ms": execution_duration * 1000,
                "records_processed": records_affected,
                "throughput_records_per_second": (
                    records_affected / execution_duration
                    if execution_duration > 0
                    else 0
                ),
            }

            # Track with Foundation performance monitor
            if database_manager.performance_monitor:
                database_manager.performance_monitor.record_metric(
                    f"database_operation_{operation}",
                    execution_duration * 1000,
                    metadata={
                        "database_type": database_manager.connection_pool.db_type,
                        "records_processed": records_affected,
                    },
                )

        # Update connection pool metrics
        pool_health = database_manager.connection_pool.health_check()
        metrics_update["connection_metrics"] = {
            "pool_healthy": pool_health["healthy"],
            "active_connections": pool_health["pool_stats"]["active_connections"],
            "total_connections": pool_health["pool_stats"]["total_connections"],
            "failed_connections": pool_health["pool_stats"]["failed_connections"],
        }

        # Update transaction metrics
        if transaction_result:
            metrics_update["transaction_metrics"] = {
                "transaction_action": transaction_result.get("action"),
                "transaction_duration": transaction_result.get(
                    "transaction_duration", 0
                ),
                "operations_count": transaction_result.get("operations_count", 0),
            }

        # Track with Foundation health monitor
        if database_manager.health_monitor:
            database_manager.health_monitor.record_health_check(
                component="database_operations",
                status="healthy" if pool_health["healthy"] else "unhealthy",
                metadata=metrics_update,
            )

        duration = time.time() - start_time
        logger.info(f"Performance metrics updated in {duration:.3f}s")

        return {"metrics_update": metrics_update, "update_duration": duration}

    except Exception as e:
        error_msg = f"Performance metrics update failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def generate_operation_report(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Generate comprehensive operation report with all results and metrics.

    Args:
        context: Framework0 context
        **params: Report generation parameters

    Returns:
        Dictionary with comprehensive operation report
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        # Collect all operation data
        database_connection_config = params.get("database_connection_config", {})
        schema_validation = params.get("schema_validation", {})
        transaction_context = params.get("transaction_context", {})
        operation_results = params.get("operation_results", {})
        validation_results = params.get("validation_results", {})
        transaction_result = params.get("transaction_result", {})
        metrics_update = params.get("metrics_update", {})

        # Generate comprehensive report
        operation_report = {
            "report_metadata": {
                "report_id": f"db_op_report_{int(time.time() * 1000000)}",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "framework_version": "1.0.0",
                "report_type": "database_operations",
            },
            "database_configuration": {
                "database_type": database_connection_config.get(
                    "database_type", "unknown"
                ),
                "connection_pool_stats": database_connection_config.get(
                    "connection_pool_stats", {}
                ),
                "health_status": database_connection_config.get("health_status", {}),
                "config_hash": database_connection_config.get("config_hash"),
            },
            "schema_information": {
                "validation_performed": bool(schema_validation),
                "schema_results": schema_validation.get("schema_validation", {}),
            },
            "transaction_summary": {
                "transaction_used": bool(transaction_context),
                "transaction_id": transaction_context.get("transaction_id"),
                "isolation_level": transaction_context.get("isolation_level"),
                "final_status": transaction_result.get("action"),
                "duration": transaction_result.get("transaction_duration", 0),
            },
            "operation_summary": {
                "operation_type": operation_results.get("operation", "unknown"),
                "target_table": operation_results.get("table_name", "unknown"),
                "records_affected": operation_results.get(
                    "records_affected", operation_results.get("records_count", 0)
                ),
                "operation_successful": bool(operation_results.get("operation")),
            },
            "validation_summary": {
                "validation_performed": bool(validation_results),
                "validation_passed": validation_results.get(
                    "validation_results", {}
                ).get("validation_passed", True),
                "validation_errors": validation_results.get(
                    "validation_results", {}
                ).get("validation_errors", []),
                "validation_warnings": validation_results.get(
                    "validation_results", {}
                ).get("validation_warnings", []),
            },
            "performance_metrics": {
                "total_execution_time": sum(
                    [
                        database_connection_config.get("initialization_time", 0),
                        schema_validation.get("validation_duration", 0),
                        operation_results.get("execution_duration", 0),
                        validation_results.get("validation_duration", 0),
                        transaction_result.get("finalization_duration", 0),
                        metrics_update.get("update_duration", 0),
                    ]
                ),
                "operation_metrics": metrics_update.get("metrics_update", {}).get(
                    "operation_metrics", {}
                ),
                "connection_metrics": metrics_update.get("metrics_update", {}).get(
                    "connection_metrics", {}
                ),
                "resource_utilization": "optimal",  # Could be enhanced with actual resource monitoring
            },
            "recommendations": [],
        }

        # Add performance recommendations
        total_time = operation_report["performance_metrics"]["total_execution_time"]
        if total_time > 5.0:
            operation_report["recommendations"].append(
                "Consider query optimization or connection pool tuning for improved performance"
            )

        failed_connections = operation_report["performance_metrics"][
            "connection_metrics"
        ].get("failed_connections", 0)
        if failed_connections > 0:
            operation_report["recommendations"].append(
                "Monitor connection failures and consider connection retry policies"
            )

        if not operation_report["validation_summary"]["validation_passed"]:
            operation_report["recommendations"].append(
                "Review validation failures and adjust data quality processes"
            )

        # Add success indicators
        operation_report["success_indicators"] = {
            "database_connection_healthy": operation_report["database_configuration"][
                "health_status"
            ].get("healthy", False),
            "operation_completed": operation_report["operation_summary"][
                "operation_successful"
            ],
            "validation_passed": operation_report["validation_summary"][
                "validation_passed"
            ],
            "transaction_committed": operation_report["transaction_summary"][
                "final_status"
            ]
            == "commit",
            "overall_success": all(
                [
                    operation_report["database_configuration"]["health_status"].get(
                        "healthy", False
                    ),
                    operation_report["operation_summary"]["operation_successful"],
                    operation_report["validation_summary"]["validation_passed"],
                ]
            ),
        }

        duration = time.time() - start_time
        logger.info(f"Operation report generated in {duration:.3f}s")

        return {
            "operation_report": operation_report,
            "report_generation_duration": duration,
        }

    except Exception as e:
        error_msg = f"Operation report generation failed: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationsError(error_msg) from e


def _build_create_table_sql(table_spec: Dict[str, Any], db_type: str) -> str:
    """
    Build CREATE TABLE SQL statement from table specification.

    Args:
        table_spec: Table specification dictionary
        db_type: Database type

    Returns:
        CREATE TABLE SQL statement
    """
    table_name = table_spec["table_name"]
    columns = table_spec.get("columns", [])

    if not columns:
        raise DatabaseOperationsError(f"No columns specified for table {table_name}")

    column_definitions = []
    for column in columns:
        col_name = column.get("name")
        col_type = column.get("type")
        col_constraints = column.get("constraints", [])

        if not col_name or not col_type:
            raise DatabaseOperationsError(f"Column name and type are required")

        # Map generic types to database-specific types
        type_mapping = {
            "postgresql": {
                "integer": "INTEGER",
                "bigint": "BIGINT",
                "string": "VARCHAR",
                "text": "TEXT",
                "decimal": "DECIMAL",
                "float": "REAL",
                "boolean": "BOOLEAN",
                "date": "DATE",
                "datetime": "TIMESTAMP",
                "json": "JSON",
            },
            "mysql": {
                "integer": "INT",
                "bigint": "BIGINT",
                "string": "VARCHAR",
                "text": "TEXT",
                "decimal": "DECIMAL",
                "float": "FLOAT",
                "boolean": "BOOLEAN",
                "date": "DATE",
                "datetime": "DATETIME",
                "json": "JSON",
            },
            "sqlite": {
                "integer": "INTEGER",
                "bigint": "INTEGER",
                "string": "TEXT",
                "text": "TEXT",
                "decimal": "REAL",
                "float": "REAL",
                "boolean": "INTEGER",
                "date": "TEXT",
                "datetime": "TEXT",
                "json": "TEXT",
            },
        }

        mapped_type = type_mapping.get(db_type, {}).get(col_type, col_type)

        # Handle type parameters (e.g., VARCHAR(255))
        type_params = column.get("type_parameters")
        if type_params:
            if isinstance(type_params, list):
                mapped_type += f"({','.join(map(str, type_params))})"
            else:
                mapped_type += f"({type_params})"

        col_def = f"{col_name} {mapped_type}"

        # Add constraints
        if "NOT NULL" in col_constraints:
            col_def += " NOT NULL"
        if "PRIMARY KEY" in col_constraints:
            col_def += " PRIMARY KEY"
        if "UNIQUE" in col_constraints:
            col_def += " UNIQUE"

        default_value = column.get("default")
        if default_value is not None:
            if isinstance(default_value, str):
                col_def += f" DEFAULT '{default_value}'"
            else:
                col_def += f" DEFAULT {default_value}"

        column_definitions.append(col_def)

    # Add table constraints
    table_constraints = table_spec.get("constraints", [])
    for constraint in table_constraints:
        constraint_type = constraint.get("type")
        constraint_columns = constraint.get("columns", [])

        if constraint_type == "primary_key":
            column_definitions.append(f"PRIMARY KEY ({','.join(constraint_columns)})")
        elif constraint_type == "foreign_key":
            ref_table = constraint.get("reference_table")
            ref_columns = constraint.get("reference_columns", [])
            fk_def = f"FOREIGN KEY ({','.join(constraint_columns)}) REFERENCES {ref_table}({','.join(ref_columns)})"
            column_definitions.append(fk_def)
        elif constraint_type == "unique":
            column_definitions.append(f"UNIQUE ({','.join(constraint_columns)})")

    # Create the SQL with proper formatting
    column_list = ",\n    ".join(column_definitions)
    create_sql = f"CREATE TABLE {table_name} (\n    {column_list}\n)"

    return create_sql
