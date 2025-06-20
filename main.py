from pydantic import BaseModel
from ray import serve
from transformers import pipeline

from common.framework import app


class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50


class GenerateResponse(BaseModel):
    text: str


@serve.deployment
@serve.ingress(app)
class ModelDeployment:
    def __init__(self):
        self.generator = pipeline("text-generation", model="distilgpt2")

    @app.post("/generate")
    async def generate(self, request: GenerateRequest):
        generated_text = self.generator(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            num_return_sequences=1,
        )[0]["generated_text"]
        return GenerateResponse(text=generated_text)


model = ModelDeployment.bind()
