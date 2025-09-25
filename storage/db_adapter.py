# storage/db_adapter.py

"""
Database Adapter for Framework0.

This module provides a unified interface to interact with various relational
databases (e.g., PostgreSQL, MySQL, SQLite) using SQLAlchemy. It abstracts
database operations, ensuring compatibility and flexibility across different
database systems.

Features:
- `DatabaseAdapter`: A class that encapsulates database connection and operations.
- Supports multiple database backends via SQLAlchemy.
- Provides methods for CRUD operations and schema inspection.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

Base = declarative_base()

class DatabaseAdapter:
    """
    A class that encapsulates database connection and operations.

    Attributes:
        engine (Engine): The SQLAlchemy engine instance.
        Session (sessionmaker): The sessionmaker factory.
        metadata (MetaData): The metadata instance for schema operations.

    Methods:
        connect(database_url: str): Establishes a connection to the database.
        disconnect(): Closes the database connection.
        create_session(): Creates a new session for database operations.
        execute_query(query: str, params: dict = None): Executes a raw SQL query.
        create_table(table_class: Base): Creates a table based on the provided class.
        drop_table(table_class: Base): Drops the table corresponding to the provided class.
    """

    def __init__(self):
        """
        Initializes the DatabaseAdapter instance.
        """
        self.engine = None
        self.Session = None
        self.metadata = MetaData()

    def connect(self, database_url: str):
        """
        Establishes a connection to the database.

        Args:
            database_url (str): The database connection URL.

        Raises:
            SQLAlchemyError: If the connection fails.
        """
        try:
            self.engine = create_engine(database_url, echo=True)
            self.Session = sessionmaker(bind=self.engine)
            Base.metadata.bind = self.engine
            logger.info(f"Connected to database at {database_url}")
        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def disconnect(self):
        """
        Closes the database connection.

        Raises:
            SQLAlchemyError: If there is an error during disconnection.
        """
        try:
            if self.engine:
                self.engine.dispose()
                logger.info("Disconnected from database")
        except SQLAlchemyError as e:
            logger.error(f"Failed to disconnect from database: {e}")
            raise

    def create_session(self):
        """
        Creates a new session for database operations.

        Returns:
            Session: A new SQLAlchemy session.

        Raises:
            SQLAlchemyError: If session creation fails.
        """
        try:
            session = self.Session()
            logger.debug("Created new database session")
            return session
        except SQLAlchemyError as e:
            logger.error(f"Failed to create session: {e}")
            raise

    def execute_query(self, query: str, params: dict = None):
        """
        Executes a raw SQL query.

        Args:
            query (str): The SQL query to execute.
            params (dict, optional): Parameters to bind to the query.

        Returns:
            ResultProxy: The result of the query execution.

        Raises:
            SQLAlchemyError: If query execution fails.
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(query, params or {})
                logger.debug(f"Executed query: {query}")
                return result
        except SQLAlchemyError as e:
            logger.error(f"Failed to execute query: {e}")
            raise

    def create_table(self, table_class: Base):
        """
        Creates a table based on the provided class.

        Args:
            table_class (Base): The class representing the table.

        Raises:
            SQLAlchemyError: If table creation fails.
        """
        try:
            table_class.metadata.create_all(self.engine)
            logger.info(f"Created table {table_class.__tablename__}")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create table {table_class.__tablename__}: {e}")
            raise

    def drop_table(self, table_class: Base):
        """
        Drops the table corresponding to the provided class.

        Args:
            table_class (Base): The class representing the table.

        Raises:
            SQLAlchemyError: If table dropping fails.
        """
        try:
            table_class.metadata.drop_all(self.engine)
            logger.info(f"Dropped table {table_class.__tablename__}")
        except SQLAlchemyError as e:
            logger.error(f"Failed to drop table {table_class.__tablename__}: {e}")
            raise
