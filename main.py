from fastapi import FastAPI
from db.base import database
from endpoints import vectors
import uvicorn

app = FastAPI(title="Vectors")
app.include_router(vectors.router, prefix="/vectors", tags=["vectors"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8100, host="0.0.0.0", reload=True)