# An Interface class for databases
class Database:
    def get_value(self, key: str):
        pass
    
    def get_name_value(self, key: str):
        pass
    
    def get_status_value(self, key: str):
        pass
    
    def delete_data(self, key: str):
        pass

    def insert(self, name: str, status: bool):
        pass

    def update_status(self, id: int, status: bool):
        pass