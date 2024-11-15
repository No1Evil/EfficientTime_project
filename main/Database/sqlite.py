import sqlite3
import tkinter as tk
from tkinter import messagebox

class Database_sqlite:
    def __init__(self, database_name: str, table_name: str):
        self.conn = create_connection(database_name)
        self.c = self.conn.cursor()
        self.table_name = table_name
        self.__create_table_if_doesnt_exist__()
    
    def __create_table_if_doesnt_exist__(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            ülesanne TEXT NOT NULL,
            staatus BOOLEAN NOT NULL
            )''')
        self.conn.commit()

        
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



# Example usage:
# conn = create_connection("example.db")
# data = {"column1": "value1", "column2": "value2"}
# insert_data(conn, "table_name", data)