from repository.vectors import VectorRepository
from db.base import database


def get_vector_repository() -> VectorRepository:
    return VectorRepository(database)