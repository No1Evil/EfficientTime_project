import sqlite3

class Database_sqlite:
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

    def insert(self, column1, column2, key, value):
        self.c.execute(f"INSERT INTO {self.table_name} ({column1}, {column2}) VALUES (?, ?)", (key, value))
        self.conn.commit()
    
    def update_value(self, column, column1, value, key):
        self.c.execute(f"UPDATE {self.table_name} SET {column} = ? WHERE {column1} = ?", (value, key))
        self.conn.commit()

    def __do_action(self, action: str, column: str, id: int):
        return self.c.execute(f"{action} {column} FROM {self.table_name} WHERE id = ?", (id,))

    def get_value(self, column, id):
        return self.__do_action("SELECT", column, id)
    
    def get_name_value(self, id):
        return self.get_value("name", id).fetchone()[0]
    
    def get_status_value(self, id):
        return self.get_value("status", id).fetchone()[0]

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

def insert_data(conn, table, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({', '.join([f'{k} TEXT' for k in data.keys()])})")
    cur.execute(sql, tuple(data.values()))
    conn.commit()
    return cur.lastrowid