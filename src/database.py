from pymongo import MongoClient
from config.config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client['twitter_trends']
        self.collection = self.db['trending_topics']

    def insert_trends(self, data):
        return self.collection.insert_one(data)

    def get_latest_trends(self):
        return self.collection.find_one(sort=[('datetime', -1)])