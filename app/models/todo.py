from typing import List
from sqlite3 import Row
from .base_model import BaseModel

class ToDo(BaseModel):
    """Model for todo items."""
    
    TABLE_NAME = 'todos'
    
    def __init__(self):
        """Initialize the ToDo model and create the table if it doesn't exist."""
        super().__init__(self.TABLE_NAME)
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT', 
            'text TEXT NOT NULL',
            'state INTEGER NOT NULL DEFAULT 0',
            'created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'
        ])
        
    def get_active_todos(self) -> List[Row]:
        """Get all active (not completed) todos."""
        return self.select_data(where={"state": 0})
        
    def get_completed_todos(self) -> List[Row]:
        """Get all completed todos."""
        return self.select_data(where={"state": 1})