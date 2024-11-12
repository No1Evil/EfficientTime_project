import sqlite3

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