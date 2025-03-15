import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import bcrypt
from datetime import datetime

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = MongoClient(
            os.getenv("MONGO_URI"),
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=30000
        )
        self.db = self.client[os.getenv("DB_NAME")]
        self.users = self.db.users
        
    def create_user(self, username, password):
        if self.users.find_one({"username": username}):
            return False
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.users.insert_one({
            "username": username,
            "password": hashed,
            "preferences": {},
            "watchlist": [],
            "watched": [],
            "history": []
        })
        return True

    def authenticate_user(self, username, password):
        user = self.users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user
        return False

    def update_preferences(self, username, preferences):
        self.users.update_one(
            {"username": username},
            {"$set": {"preferences": preferences}},
            upsert=True
        )

    def add_to_history(self, username, movie_id):
        self.users.update_one(
            {"username": username},
            {"$push": {"history": {
                "movie_id": movie_id,
                "timestamp": datetime.now()
            }}},
            upsert=True
        )

    def get_user_profile(self, username):
        return self.users.find_one({"username": username})

    def add_to_watchlist(self, username, show_id):
        self.users.update_one(
            {"username": username},
            {"$addToSet": {"watchlist": show_id}},
            upsert=True
        )

    def mark_as_watched(self, username, show_id):
        self.users.update_one(
            {"username": username},
            {"$pull": {"watchlist": show_id}, "$addToSet": {"watched": show_id}},
            upsert=True
        )

    def get_watchlist(self, username):
        user = self.users.find_one({"username": username})
        return user.get("watchlist", []) if user else []

    def get_watched(self, username):
        user = self.users.find_one({"username": username})
        return user.get("watched", []) if user else []

auth_db = MongoDB()
