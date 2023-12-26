from .base_model import BaseModel

class Action(BaseModel):
    def __init__(self):
        super().__init__('actions')
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT', 
            'type TEXT NOT NULL',
            'ip TEXT NOT NULL',
            'details TEXT',
            'created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'
        ])