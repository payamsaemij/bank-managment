
from contextlib import asynccontextmanager
# Import all models so they are registered with the shared Base.metadata.
from app.db import models  # noqa: F401
from fastapi import FastAPI
from app.features.customers.router import router as customers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Banking System API is starting up...")
    yield
    print("Banking System API is shutting down...")


app = FastAPI(
    title="Banking System API",
    description="A Banking System API built with FastAPI.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(customers_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
