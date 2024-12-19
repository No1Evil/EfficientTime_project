from window.window import Window
from Database.sqlite import *
from Database.database_json import *

def change_database(db_type: str):
    global db
    if db_type == "sqlite":
        db = Database_sqlite("EfficientTime_project/database/sqlite.db", "ülesanded")
    else:
        db = Database_json("EfficientTime_project/database/json.json")

def main():
    user_input = input("Choose database type (sqlite/json): ")
    change_database(user_input)
    window = Window("EfficientTime", db)

if __name__ == "__main__":
    main()