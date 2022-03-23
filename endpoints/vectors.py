from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.vector import Vector, VectorIn, VectorForResponse
from repository.vectors import VectorRepository
from .depends import get_vector_repository

router = APIRouter()


@router.get("/getAll", response_model=List[VectorForResponse])
async def get_all(
        vectors: VectorRepository = Depends(get_vector_repository),
        limit: int = 100,
        skip: int = 0):
    return await vectors.get_all(limit=limit, skip=skip)


@router.get("/getById", response_model=VectorForResponse)
async def get_by_id(
        id: int,
        vectors: VectorRepository = Depends(get_vector_repository)):
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Vector with id {id} not found")
    result = await vectors.get_by_id(id=id)
    if result is None:
        raise not_found_exception
    return result


@router.get("/recognizeByPhoto", response_model=VectorForResponse)
async def recognize_by_photo(
        vectors: VectorRepository = Depends(get_vector_repository)):
    return await vectors.recognize_by_photo()


@router.post("/createOne", response_model=VectorForResponse)
async def create_one(
        vectors: VectorRepository = Depends(get_vector_repository)):
    return await vectors.create_one()


@router.post("/uploadAll")
async def upload_images_for_recognition(
        vectors: VectorRepository = Depends(get_vector_repository)):
    await vectors.upload_images_for_recognition()
    return {"All photos was recognized and inserted"}


@router.delete("/deleteOne")
async def delete_one(
        id: int,
        vectors: VectorRepository = Depends(get_vector_repository)):
    vector = await vectors.get_by_id(id=id)
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Vector with id {id} not found")
    if vector is None:
        raise not_found_exception
    await vectors.delete_one(id=id)
    return {f"Record with {id} was deleted"}


@router.delete("/deleteAll")
async def delete_all(
        vectors: VectorRepository = Depends(get_vector_repository)):
    await vectors.delete_all()
    return {"All records was deleted"}
