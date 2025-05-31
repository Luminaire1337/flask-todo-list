import sqlite3
import os
import threading
from contextlib import contextmanager

class DatabaseConnection:
    """Thread-safe database connection manager for SQLite."""
    # Use thread local storage to prevent cross-thread connection usage
    _local = threading.local()
    
    @classmethod
    def get_db_path(cls, file_name: str = "database.db") -> str:
        """Get the database file path, respecting environment variable if set."""
        db_path = os.environ.get("FLASK_DB_PATH", file_name)
        return db_path
    
    @classmethod
    def open(cls, file_name: str = "database.db") -> sqlite3.Connection:
        """
        Open a database connection specific to the current thread.
        
        SQLite connections can only be used in the thread they were created in,
        so we store connections in thread-local storage.
        """
        # Initialize the thread-local storage if needed
        if not hasattr(cls._local, 'connections'):
            cls._local.connections = {}
            
        db_path = cls.get_db_path(file_name)
        
        # Check if we already have a connection for this thread and path
        if db_path in cls._local.connections:
            return cls._local.connections[db_path]

        # Create a new connection for this thread
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        
        # Store it in the thread-local storage
        cls._local.connections[db_path] = connection
        return connection
    
    @classmethod
    def close(cls, file_name: str = "database.db") -> bool:
        """Close a database connection for the current thread."""
        if not hasattr(cls._local, 'connections'):
            return False
            
        db_path = cls.get_db_path(file_name)
        
        if db_path in cls._local.connections:
            cls._local.connections[db_path].close()
            del cls._local.connections[db_path]
            return True
        
        return False
        
    @classmethod
    def close_all(cls) -> None:
        """Close all connections for the current thread."""
        if not hasattr(cls._local, 'connections'):
            return
            
        for path, conn in list(cls._local.connections.items()):
            conn.close()
            
        cls._local.connections = {}
        
    @classmethod
    @contextmanager
    def connection(cls, file_name: str = "database.db"):
        """
        Context manager for database connections that ensures thread safety.
        
        Each thread will get its own connection.
        """
        conn = cls.open(file_name)
        try:
            yield conn
            conn.commit()  # Auto-commit at the end of the context
        except Exception:
            conn.rollback()  # Rollback on exception
            raise
        finally:
            # We don't close the connection here - it will be reused within the same thread
            # and closed when the app shuts down or when close() is explicitly called
            pass
            
    @classmethod
    @contextmanager
    def cursor(cls, file_name: str = "database.db"):
        """
        Context manager for database cursors that ensures thread safety.
        
        Each thread will get its own cursor from its own connection.
        """
        conn = cls.open(file_name)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()  # Auto-commit at the end of the context
        except Exception:
            conn.rollback()  # Rollback on exception
            raise
        finally:
            cursor.close()  # Always close the cursor
