import urllib.parse

import pymongo

MONGO_HOST = "nanchuan.site"
MONGO_PORT = 2708
MONGO_AUTHENTICATION_DATABASE = "hjxh-operate"
MONGO_DATABASE_NAME = "hjxh-operate"
MONGO_USERNAME = 'hjxh-operator'
MONGO_PASSWORD = "hjxh-operator"

username = urllib.parse.quote_plus(MONGO_USERNAME)
password = urllib.parse.quote_plus(MONGO_PASSWORD)
MONGO_URI = f'mongodb://{username}:{password}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE_NAME}?authSource={MONGO_AUTHENTICATION_DATABASE}'

client = pymongo.MongoClient(MONGO_URI)

db = client[MONGO_DATABASE_NAME]


if __name__ == '__main__':
    print(db.list_collection_names())


