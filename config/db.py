from pymongo import MongoClient
from config.settings import *

class MongoDB:
    _client = None

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.client = None
        self.db = None

    def __enter__(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client[self.db_name]
            print(f"Connected to MongoDB database: {self.db_name}")
            return self.db
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()
            print(f"MongoDB connection to {self.db_name} closed.")