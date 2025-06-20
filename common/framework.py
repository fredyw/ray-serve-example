import time
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request

app = FastAPI()


class Health(BaseModel):
    status: str


@app.get("/health")
async def health() -> Health:
    return Health(status="OK")


class Version(BaseModel):
    version: str


@app.get("/version")
async def version() -> Version:
    return Version(version="0.1.0")


@app.middleware("http")
async def response_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    process_time = end_time - start_time
    response.headers["x-response-time"] = f"{process_time}"
    return response


@app.middleware("http")
async def trace_id(request: Request, call_next):
    response = await call_next(request)
    if "x-trace-id" in request.headers:
        response.headers["x-trace-id"] = request.headers["x-trace-id"]
    return response
