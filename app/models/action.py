from typing import List
from sqlite3 import Row
from .base_model import BaseModel

class Action(BaseModel):
    """Model for logging user actions."""
    
    TABLE_NAME = 'actions'
    
    # Action types
    ACTION_CREATE = 'todo-create'
    ACTION_UPDATE = 'todo-update'
    ACTION_DELETE = 'todo-delete'
    ACTION_EXPORT = 'export'
    
    def __init__(self):
        """Initialize the Action model and create the table if it doesn't exist."""
        super().__init__(self.TABLE_NAME)
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT', 
            'type TEXT NOT NULL',
            'ip TEXT NOT NULL',
            'details TEXT',
            'created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'
        ])
        
    def log_action(self, action_type: str, ip_address: str, details: str) -> int | None:
        """Log a user action."""
        return self.insert_data({
            'type': action_type,
            'ip': ip_address,
            'details': details
        })
        
    def get_recent_actions(self, limit: int = 100) -> List[Row]:
        """Get the most recent actions."""
        return self.select_data(limit=limit)