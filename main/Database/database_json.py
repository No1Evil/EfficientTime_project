import os
import json

class Database_json():
    def __init__(self):
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

    def insert_data(self, task_id: int, name: str, status: bool):
        self.json[task_id] = {"name": name, "status": status}
        self.__save_database__()
    
    def get_value(self, key: str):
        return self.json.get(key)
    
    def get_name_value(self, key: str):
        return self.get_value(key)["name"]
    
    def get_status_value(self, key: str):
        return self.get_value(key)["status"]
    
    def delete_data(self, key: str):
        self.json.pop(key)
        self.__save_database__()
    
db = Database_json("EfficientTime_project/database/json.json")
print(db.absoule_path)