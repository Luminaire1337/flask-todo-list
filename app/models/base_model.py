from app.utils import DatabaseConnection

class BaseModel:
    def __init__(self, table_name):
        self._database_connection = DatabaseConnection.open()
        self._database_cursor = self._database_connection.cursor()
        self.table_name = table_name

    def __del__(self):
        DatabaseConnection.close()

    def create_table(self, columns: list) -> None:
        columns_string = ', '.join(columns)
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_string})'
        self._database_cursor.execute(query)
        self._database_connection.commit()

    def insert_data(self, data: dict) -> None:
        columns = ', '.join([key for key in data.keys()])
        placeholders = ', '.join(['?' for _ in data.keys()])
        query = f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})'
        self._database_cursor.execute(query, [value for value in data.values()])
        self._database_connection.commit()

    def select_data(self, limit=0) -> list:
        query = f'SELECT * FROM {self.table_name}'
        if limit > 0:
            query += f' LIMIT {limit}'

        self._database_cursor.execute(query)
        return self._database_cursor.fetchall()

    def _generate_parameters_string(self, parameters: dict, delimiter="AND ") -> str:
        return delimiter.join([f'{key} = ?' for key in parameters.keys()])
    
    def find_data(self, query_parameters: dict, limit=0) -> list:
        query = f'SELECT * FROM {self.table_name} WHERE {self._generate_parameters_string(query_parameters)}'
        if limit > 0:
            query += f' LIMIT {limit}'

        self._database_cursor.execute(query, [value for value in query_parameters.values()])
        return self._database_cursor.fetchall()
    
    def update_data(self, data: dict, query_parameters: dict) -> None:
        query = f'UPDATE {self.table_name} SET {self._generate_parameters_string(data, ", ")} WHERE {self._generate_parameters_string(query_parameters)}'
        self._database_cursor.execute(query, [value for value in data.values()] + [value for value in query_parameters.values()])
        self._database_connection.commit()

    def delete_data(self, query_parameters: dict) -> None:
        query = f'DELETE FROM {self.table_name} WHERE {self._generate_parameters_string(query_parameters)}'
        self._database_cursor.execute(query, [value for value in query_parameters.values()])
        self._database_connection.commit()