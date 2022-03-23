import datetime
from typing import Optional
from pydantic import BaseModel


class Vector(BaseModel):
    id: Optional[int] = None
    image_name: str
    vector: bytes


class VectorIn(BaseModel):
    image_name: str
    vector: bytes


class VectorForResponse(BaseModel):
    id: Optional[int] = None
    image_name: str
