import pymongo

from settings import MONGO_DATABASE_NAME, MONGO_URI

client = pymongo.MongoClient(MONGO_URI)

db = client[MONGO_DATABASE_NAME]


if __name__ == '__main__':
    print(db.list_collection_names())


