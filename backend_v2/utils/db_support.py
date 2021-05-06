from typing import TypedDict, Any

import demjson
from fastapi import HTTPException

from database.client import db


class AjaxResult(TypedDict, total=False):
    success: bool
    result: Any
    msg: Any


def db_general_query(coll_name: str, query: str = None, skip: int = 0, limit: int = 10,
                     sort: str = None) -> AjaxResult:
    """
    refer: Advanced Dependencies - FastAPI - https://fastapi.tiangolo.com/advanced/advanced-dependencies/
    """
    if sort:
        try:
            sort = [*demjson.decode(f'{sort}').items()]
        except Exception as e:
            raise HTTPException(400, detail='sort不符合格式：' + e.__str__())
    
    if query:
        try:
            query = demjson.decode(f"{query}", )
        except Exception as e:
            raise HTTPException(400, detail='query不符合格式：' + e.__str__())
    cursor = db[coll_name].find(query, sort=sort)
    
    return {
        "success": True,
        "result": {
            "total": cursor.count(),
            "items": list(cursor.skip(skip).limit(limit))
        }
    }