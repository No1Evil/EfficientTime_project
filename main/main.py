from window.window import Window
from Database.sqlite import *
from Database.database_json import *

db = Database_json("EfficientTime_project/database/json.json")

window = Window("EfficientTime", db)