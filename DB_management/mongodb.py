from pymongo import MongoClient

from datetime import datetime

now_time = datetime.now()

client = MongoClient("mongodb://localhost:27017/")

db = client["Ascli"]

session = db["Sessions"]
session_id = 46754127

session.update_one({"_id": session_id}, {"$set"})

for chat in session.find({"_id": session_id}):
    print(chat)
