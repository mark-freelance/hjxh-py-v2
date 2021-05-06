from fastapi import APIRouter

from database.client import db

api_comments = APIRouter(prefix='/comments')

coll_comments = db['goods_comments_detail']


@api_comments.get('/')
def get_comments(limit: int = 20):
    return list(coll_comments.find({}).limit(limit))
