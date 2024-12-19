import sqlite3
from .IDatabase import Database

class Database_sqlite(Database):
    def __init__(self, database_name: str, table_name: str):
        self.conn = create_connection(database_name)
        self.c = self.conn.cursor()
        self.table_name = table_name
        self.__create_table_if_doesnt_exist()
    
    def __create_table_if_doesnt_exist(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status BOOLEAN NOT NULL
            )''')
        self.conn.commit()

    def insert(self, name: str, status: bool):
        self.c.execute(f"SELECT MAX(id) FROM {self.table_name}")
        max_id = self.c.fetchone()[0]
        next_id = (max_id + 1) if max_id is not None else 1
        self.c.execute(f"INSERT INTO {self.table_name} (id, name, status) VALUES (?, ?, ?)", (next_id, name, status))
        self.conn.commit()
    
    def update_status(self, id: int, status: bool):
        self.__do_action("UPDATE", f"status = {status}", id)
        self.conn

    def __do_action(self, action: str, column: str, id: int):
        return self.c.execute(f"{action} {column} FROM {self.table_name} WHERE id = ?", (id,))

    def get_value(self, key: str):
        return self.c.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (key,)).fetchone()
    
    def get_name_value(self, key: str):
        return self.get_value(key)[1]
    
    def get_status_value(self, key: str):
        return self.get_value(key)[2]

    def delete_data(self, id: str):
        self.c.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
        self.conn.commit()
    
    def delete(self, id):
        self.__do_action("DELETE", "", id)
        self.conn.commit()
    
    def select(self, column):
        return self.c.execute(f"SELECT {column} FROM {self.table_name}")
    
    def select_all(self):
        return self.select("*")
    

        
def create_connection(db_file) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file} successfully")
    except sqlite3.Error as e:
        print(e)
    return conn