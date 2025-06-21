import pytest
import ray
import httpx
import uuid

from main import model
from ray import serve


@pytest.fixture(scope="session")
def start_ray():
    serve.run(model)
    yield
    serve.shutdown()
    ray.shutdown()


def test_version(start_ray):
    response = httpx.get("http://localhost:8000/version")
    assert len(response.headers["x-response-time"]) > 0
    assert response.json()["version"] == "0.1.0"


def test_health(start_ray):
    response = httpx.get("http://localhost:8000/health")
    assert len(response.headers["x-response-time"]) > 0
    assert response.json()["status"] == "OK"


def test_generate(start_ray):
    trace_id = str(uuid.uuid4())
    response = httpx.post(
        "http://localhost:8000/generate",
        headers={"x-trace-id": trace_id},
        json={
            "prompt": "Tell me a short story about a brave knight and a dragon.",
            "max_new_tokens": 100,
        },
    )
    assert len(response.headers["x-response-time"]) > 0
    assert response.headers["x-trace-id"] == trace_id
    assert len(response.json()["text"]) > 0
