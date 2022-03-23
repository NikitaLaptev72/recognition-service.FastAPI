import sqlalchemy
from .base import metadata

vectors = sqlalchemy.Table(
    "vector",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("image_name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("vector", sqlalchemy.PickleType)
)
