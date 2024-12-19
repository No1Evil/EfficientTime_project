from window.window import Window
from Database.sqlite import *
from Database.database_json import *

db = Database_json("EfficientTime_project/database/json.json")
data_sqlite = Database_sqlite("EfficientTime_project/database/sqlite.db", "ülesanded")

window = Window("EfficientTime", db)