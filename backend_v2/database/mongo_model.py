from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

"""
reference:
1. https://github.com/tiangolo/fastapi/issues/452
2. https://github.com/tiangolo/fastapi/issues/1515
"""


class PyObjectId(ObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId]
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        # dict_encoders = {str: lambda x: ObjectId(x) if ObjectId.is_valid(x) else x}
        dict_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }


class MongoOutModel(MongoBaseModel):
    
    def __init__(self, **pydict):
        super().__init__(**pydict)
        self.id = pydict.pop('_id')
