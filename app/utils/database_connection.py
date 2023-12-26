import sqlite3

class DatabaseConnection:
    _instances = {}
    _open_instances = []

    @classmethod
    def open(cls, file_name="database.db") -> sqlite3.Connection:
        instance = cls._instances.get(file_name)
        if instance:
            return instance

        connection = sqlite3.connect(file_name)
        connection.row_factory = sqlite3.Row

        cls._instances[file_name] = connection
        cls._open_instances.append(file_name)
        return cls._instances[file_name]
    
    @classmethod
    def close(cls, file_name="database.db") -> bool:
        cls._open_instances.remove(file_name)
        if cls._open_instances.count(file_name) == 0:
            cls._instances.get(file_name).close()
            cls._instances.pop(file_name)
            return True
        
        return False