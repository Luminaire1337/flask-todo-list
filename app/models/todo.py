from .base_model import BaseModel

class ToDo(BaseModel):
    def __init__(self):
        super().__init__('todos')
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT', 
            'text TEXT NOT NULL',
            'state INTEGER NOT NULL DEFAULT 0',
            'created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'
        ])