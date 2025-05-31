from typing import List, Dict, Any, Optional
from sqlite3 import Row
from app.utils import DatabaseConnection

class BaseModel:
    def __init__(self, table_name: str):
        """Initialize a new model with a table name."""
        self.table_name = table_name
        
    def create_table(self, columns: List[str]) -> None:
        """Create a new table if it doesn't exist."""
        columns_string = ', '.join(columns)
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_string})'
        
        with DatabaseConnection.cursor() as cursor:
            cursor.execute(query)

    def insert_data(self, data: Dict[str, Any]) -> int | None:
        """Insert data into the table and return the ID of the inserted row."""
        if not data:
            return 0
            
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.keys()])
        query = f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})'
        
        with DatabaseConnection.cursor() as cursor:
            cursor.execute(query, list(data.values()))
            return cursor.lastrowid

    def select_data(self, limit: int = 0, where: Optional[Dict[str, Any]] = None) -> List[Row]:
        """Select data from the table with optional limit and where clause."""
        query = f'SELECT * FROM {self.table_name}'
        params = []
        
        if where:
            conditions = []
            for key, value in where.items():
                conditions.append(f"{key} = ?")
                params.append(value)
            
            if conditions:
                query += f" WHERE {' AND '.join(conditions)}"
        
        if limit > 0:
            query += f' LIMIT {limit}'

        with DatabaseConnection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def _generate_parameters_string(self, parameters: Dict[str, Any], delimiter: str = "AND ") -> str:
        """Generate a parameters string for SQL queries."""
        return delimiter.join([f'{key} = ?' for key in parameters.keys()])
    
    def find_data(self, query_parameters: Dict[str, Any], limit: int = 0) -> List[Row]:
        """Find data in the table based on query parameters."""
        query = f'SELECT * FROM {self.table_name} WHERE {self._generate_parameters_string(query_parameters)}'
        if limit > 0:
            query += f' LIMIT {limit}'

        with DatabaseConnection.cursor() as cursor:
            cursor.execute(query, list(query_parameters.values()))
            return cursor.fetchall()
    
    def update_data(self, data: Dict[str, Any], query_parameters: Dict[str, Any]) -> int:
        """Update data in the table based on query parameters."""
        query = f'UPDATE {self.table_name} SET {self._generate_parameters_string(data, ", ")} WHERE {self._generate_parameters_string(query_parameters)}'
        params = list(data.values()) + list(query_parameters.values())
        
        with DatabaseConnection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    def delete_data(self, query_parameters: Dict[str, Any]) -> int:
        """Delete data from the table based on query parameters."""
        query = f'DELETE FROM {self.table_name} WHERE {self._generate_parameters_string(query_parameters)}'
        
        with DatabaseConnection.cursor() as cursor:
            cursor.execute(query, list(query_parameters.values()))
            return cursor.rowcount
            
    def execute_query(self, query: str, params: Optional[List[Any]] = None) -> List[Row]:
        """Execute a custom query and return the results."""
        with DatabaseConnection.cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor.fetchall()
        self._database_cursor.execute(query, [value for value in query_parameters.values()])
        self._database_connection.commit()