from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["Ascli"]

sessions = db["Sessions"]

x = sessions.find({}, {"_id": 1})

for i in x:
    print(i)
