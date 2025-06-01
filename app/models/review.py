from typing import List
from sqlite3 import Row
from .base_model import BaseModel

class Review(BaseModel):
    """Model for review items."""
    
    TABLE_NAME = 'reviews'
    
    def __init__(self):
        """Initialize the Review model and create the table if it doesn't exist."""
        super().__init__(self.TABLE_NAME)
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT', 
            'username TEXT NOT NULL',
            'title TEXT NOT NULL',
            'content TEXT NOT NULL',
            'rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5)',
            'created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'
        ])