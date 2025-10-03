# orchestrator/context/version_control.py
# This module implements the VersionControl class, which provides database-based
# versioning for contexts and recipes in the IAF0 framework.
# It uses SQLAlchemy for ORM and database interactions, and Alembic for schema migrations.
# Versioning allows tracking changes over time, with features like commits (saving a snapshot),
# rollbacks (reverting to a previous version), and retrieving specific versions.
# This integrates with storage/db_adapter.py for actual DB operations and context.py for data access.
# Diffs are handled via storage/diff_viewer.py, but this class focuses on version management.
# Each version is stored with metadata like version_id, parent_version, timestamp, and serialized data.

import datetime  # Imported for timestamping versions with current date/time.
from typing import Any, Dict, Optional, List  # Imported for type hints to enhance code clarity and static analysis.
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey  # Imported from SQLAlchemy for defining database models and engine.
from sqlalchemy.ext.declarative import declarative_base  # Imported to create a base class for declarative models.
from sqlalchemy.orm import sessionmaker, relationship  # Imported for ORM session management and relationships.
from storage.db_adapter import DBAdapter  # Imported to use the DBAdapter for low-level DB connections and operations.
from orchestrator.context.context import Context  # Imported to access and manipulate the Context object during versioning.

Base = declarative_base()  # Creates a base class for all SQLAlchemy models in this module.

class ContextVersion(Base):
    # Defines the SQLAlchemy model for storing context versions in the database.
    # This is a helper class used internally by VersionControl.
    __tablename__ = 'context_versions'  # Sets the database table name for this model.

    id = Column(Integer, primary_key=True)  # Defines the primary key column as an auto-incrementing integer.
    version_id = Column(String, unique=True, nullable=False)  # Defines a unique string column for the version ID (e.g., 'v1').
    parent_version = Column(String, ForeignKey('context_versions.version_id'))  # Defines a foreign key to link to parent versions for history.
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Defines a datetime column with default UTC now for when the version was created.
    data = Column(Text, nullable=False)  # Defines a text column to store the serialized JSON data of the context.

    children = relationship("ContextVersion", backref="parent", remote_side=[version_id])  # Defines a relationship for child versions (for branching if extended).

class VersionControl:
    """
    VersionControl class for DB-based versioning of contexts and recipes.
    Handles commits, rollbacks, and version retrieval.
    Requires a DBAdapter for database interactions.
    """

    def __init__(self, db_adapter: DBAdapter) -> None:
        # Initializes the VersionControl instance.
        # Requires a DBAdapter to connect to the database.
        self.db_adapter = db_adapter  # Stores the DBAdapter reference for DB operations.
        self.engine = create_engine(self.db_adapter.get_db_url())  # Creates a SQLAlchemy engine using the DB URL from the adapter.
        Base.metadata.create_all(self.engine)  # Creates all tables (like context_versions) if they don't exist, using the engine.
        self.Session = sessionmaker(bind=self.engine)  # Creates a session factory bound to the engine for ORM sessions.

    def commit(self, context: Context, version_id: Optional[str] = None, parent_version: Optional[str] = None) -> str:
        # Commits the current context state as a new version in the DB.
        # Serializes the data to JSON and stores it with metadata.
        # Args:
        #   context: The Context object to version.
        #   version_id: Optional custom version ID; auto-generates if None.
        #   parent_version: Optional parent version ID for history linking.
        # Returns: The committed version_id.
        data = context.to_dict()  # Retrieves the current context data as a dict.
        serialized_data = json.dumps(data)  # Serializes the dict to a JSON string for storage.

        if version_id is None:  # Checks if a version_id was provided.
            version_id = self._generate_version_id()  # Calls private method to auto-generate a version ID if not provided.

        session = self.Session()  # Creates a new ORM session.
        try:  # Starts a try block for transaction management.
            new_version = ContextVersion(  # Creates a new model instance.
                version_id=version_id,  # Sets the version_id.
                parent_version=parent_version,  # Sets the parent_version if provided.
                data=serialized_data  # Sets the serialized data.
            )
            session.add(new_version)  # Adds the new version to the session.
            session.commit()  # Commits the transaction to the database.
            return version_id  # Returns the version_id of the committed version.
        except Exception as e:  # Catches any exceptions during commit.
            session.rollback()  # Rolls back the transaction on error.
            raise e  # Re-raises the exception for higher-level handling.
        finally:  # Ensures the session is closed.
            session.close()  # Closes the ORM session.

    def rollback(self, version_id: str, context: Context) -> None:
        # Rolls back the context to a previous version from the DB.
        # Loads the version data and sets it in the provided context.
        # Args:
        #   version_id: The version ID to rollback to.
        #   context: The Context object to update with the rolled-back data.
        session = self.Session()  # Creates a new ORM session.
        try:  # Starts a try block for safe querying.
            version = session.query(ContextVersion).filter_by(version_id=version_id).first()  # Queries for the version by ID.
            if not version:  # Checks if the version was found.
                raise ValueError(f"Version {version_id} not found.")  # Raises error if missing.

            data = json.loads(version.data)  # Deserializes the JSON data back to a dict.
            context.clear()  # Clears the current context data.
            for key, value in data.items():  # Iterates over the loaded data.
                context.set(key, value, who="rollback")  # Sets each key-value in the context with traceability.
        finally:  # Ensures the session is closed.
            session.close()  # Closes the ORM session.

    def get_versions(self, limit: int = 10) -> List[Dict[str, Any]]:
        # Retrieves a list of recent versions with metadata.
        # Args:
        #   limit: Number of versions to return (default 10).
        # Returns: List of dicts with version details.
        session = self.Session()  # Creates a new ORM session.
        try:  # Starts a try block for querying.
            versions = session.query(ContextVersion).order_by(ContextVersion.timestamp.desc()).limit(limit).all()  # Queries recent versions, ordered by timestamp descending.
            return [  # Returns a list of dicts.
                {
                    'version_id': v.version_id,  # Includes version_id.
                    'parent_version': v.parent_version,  # Includes parent_version.
                    'timestamp': v.timestamp.isoformat()  # Includes timestamp as ISO string.
                } for v in versions  # For each version queried.
            ]
        finally:  # Ensures the session is closed.
            session.close()  # Closes the ORM session.

    def _generate_version_id(self) -> str:
        # Private method to auto-generate a unique version ID.
        # For simplicity, uses a timestamp-based ID; can be extended for UUIDs.
        # Returns: A string like 'v_YYYYMMDD_HHMMSS'.
        now = datetime.datetime.utcnow()  # Gets current UTC time.
        return f"v_{now.strftime('%Y%m%d_%H%M%S')}"  # Formats and returns the version ID string.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: Formatted string indicating the class and DB type.
        db_type = self.db_adapter.db_type if self.db_adapter else "None"  # Gets the DB type from adapter or "None".
        return f"VersionControl(db_type={db_type})"  # Returns the debug string.

# No additional code outside the class and model; this module is focused on VersionControl.
# In the framework, VersionControl is used by persistence.py during flushes to commit versions,
# and can be accessed via CLI for diffs/rollbacks (e.g., cli/commands/version.py).