from window.window import Window
from Database.sqlite import *

db = Database_sqlite("EfficientTime_project/database/sqlite3.db", "ülesanded")

window = Window("EfficientTime", db)