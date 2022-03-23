from .vectors import vectors
from .base import metadata, engine

metadata.create_all(bind=engine)
