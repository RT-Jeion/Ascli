from pymongo import MongoClient
from get_time import get_time

client = MongoClient("mongodb://localhost:27017/")

db = client["Ascli"]


print(db.list_collection_names())

time = get_time()

print(time)