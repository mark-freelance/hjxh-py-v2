import urllib.parse

MONGO_HOST = "nanchuan.site"
MONGO_PORT = 2708
MONGO_AUTHENTICATION_DATABASE = "admin"
MONGO_USERNAME = "mark"
MONGO_PASSWORD = "Mark@2019"

username = urllib.parse.quote_plus(MONGO_USERNAME)
password = urllib.parse.quote_plus(MONGO_PASSWORD)
MONGO_URI = f'mongodb://{username}:{password}@{MONGO_HOST}:{MONGO_PORT}/?authSource={MONGO_AUTHENTICATION_DATABASE}'

MONGO_DATABASE_NAME = "皇家小虎"
