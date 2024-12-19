import os
import json
from .IDatabase import Database

class Database_json(Database):
    def __init__(self, absoule_path: str):
        self.absoule_path = absoule_path
        self.json = self.__load_database__()
    
    def __load_database__(self):
        if os.path.exists(self.absoule_path):
            with open(self.absoule_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        else:
            return {}
    
    def __save_database__(self):
        with open(self.absoule_path, 'w') as file:
            json.dump(self.json, file, indent=4)

    def insert(self, name: str, status: bool):
        if self.json:
            next_key = str(max(int(k) for k in self.json.keys()) + 1)
        else:
            next_key = "1"
        self.json[next_key] = {"name": name, "status": status}
        self.__save_database__()
    
    def update_status(self, id: int, status: bool):
        self.json[str(id)]["status"] = status
        self.__save_database__()
    
    def get_value(self, key: str):
        return self.json.get(str(key))
    
    def get_name_value(self, key: str):
        return self.get_value(key)["name"]
    
    def get_status_value(self, key: str):
        return self.get_value(key)["status"]
    
    def delete_data(self, key: str):
        key = str(key)
        if key in self.json:
            self.json.pop(key)
            self.__save_database__()
        else:
            print(f"Key {key} not found in the database.")
    
    def select_all(self):
        return [(key, value["name"], value["status"]) for key, value in self.json.items()]

db = Database_json("EfficientTime_project/database/json.json")
print(db.absoule_path)