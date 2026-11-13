from pymongo import MongoClient

client = MongoClient(
    "mongodb://127.0.0.1:27017",
    serverSelectionTimeoutMS=5000,
)

database = client["ai_career_companion"]
profiles_collection = database["profiles"]

profiles_collection.create_index("email", unique=True)