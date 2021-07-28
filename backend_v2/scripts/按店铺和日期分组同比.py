import pandas as pd
import pymongo
uri = pymongo.MongoClient('mongodb://hjxh-operator:hjxh-operator@nanchuan.site:2708/hjxh-operate')
coll = uri['hjxh-operate']['V2_mall_data']
items = list(coll.aggregate([
    {"$lookup": {"from": "users", "localField": "userId", "foreignField": "userId", "as": "user"}},
    {"$addFields": {"username": {"$arrayElemAt": [ "$user.username", 0]}}},
    {"$project": {"username": 1, "amount": "$cfmOrdrAmt", "date": "$targetDate", "_id": 0}}
]))
df = pd.DataFrame(items)
df2 = df.pivot_table(index=['username'], columns=['date'], values='amount')
df2['同比'] = df2['2021-05-16'] / df2['2021-04-16'] - 1
