from db.vectors import vectors
from models.vector import Vector, VectorIn
from typing import List, Optional
from .base import BaseRepository
from recognition_logic import get_vectors_from_images, face_rec, get_vector_from_image


class VectorRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Vector]:
        query = vectors.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[Vector]:
        query = vectors.select().where(vectors.c.id == id)
        vector = await self.database.fetch_one(query)
        if vector is None:
            return None
        return Vector.parse_obj(vector)

    # async def create_one(self, v: VectorIn) -> Vector:
    #     vector = Vector(
    #         image_name=v.image_name,
    #         vector=v.vector
    #     )
    #     values = {**vector.dict()}
    #     values.pop("id", None)
    #     query = vectors.insert().values(**values)
    #     vector.id = await self.database.execute(query)
    #     return vector

    async def create_one(self) -> Vector:
        received_vector = get_vector_from_image()
        vector = Vector(
                image_name=received_vector.image_name,
                vector=received_vector.vector
            )
        values = {**vector.dict()}
        values.pop("id", None)
        query = vectors.insert().values(**values)
        vector.id = await self.database.execute(query)
        return vector

    async def delete_one(self, id: int):
        query = vectors.delete().where(vectors.c.id == id)
        return await self.database.execute(query=query)

    async def delete_all(self):
        query = vectors.delete()
        return await self.database.execute(query=query)

    async def upload_images_for_recognition(self) -> Vector:
        for item in get_vectors_from_images("/home/nikita/Desktop/Faces"):
            vector = Vector(
                image_name=item.image_name,
                vector=item.vector
            )
            values = {**vector.dict()}
            values.pop("id", None)
            query = vectors.insert().values(**values)
            vector.id = await self.database.execute(query)

    async def recognize_by_photo(self) -> List[Vector]:
        query = vectors.select()
        result = await self.database.fetch_all(query=query)
        vectors_for_recognition = []
        ids_for_recognition = []
        for i in result:
            vectors_for_recognition.append(tuple(i.values())[2])
            ids_for_recognition.append(tuple(i.values())[0])
        id = face_rec(ids_for_recognition, vectors_for_recognition)
        query = vectors.select().where(vectors.c.id == id)
        vector = await self.database.fetch_one(query)
        if vector is None:
            return None
        return Vector.parse_obj(vector)
