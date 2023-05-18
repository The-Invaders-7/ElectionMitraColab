from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://tanishq777:tanishq777@cluster0.lzgyb.mongodb.net/ElectionMitra?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)