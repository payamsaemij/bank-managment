
from fastapi import FastAPI

app = FastAPI(
    title="Banking System API",
    description="A Banking System API built with FastAPI.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
