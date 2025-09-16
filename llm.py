import requests
from typing import Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel


# ----------
# Response Schemas
# ----------
class LlmResponseSchema(BaseModel):
    model: str
    think: Optional[str]
    response: str


class Llm(ABC):
    @abstractmethod
    def invoke(self, prompt: str, system: str = None) -> LlmResponseSchema:
        raise NotImplementedError()


class Ollama(Llm):
    def __init__(self, model, thinking=False):
        self.url = "http://localhost:11434/api"
        self.model = model
        self.thinking = thinking

    def invoke(self, prompt: str, system: str = None, **options) -> LlmResponseSchema:
        messages = []

        if system is not None:
            messages = [{
                "role": "user",
                "content": system,
            }]

        messages.append({
            "role": "user",
            "content": prompt,
        })

        resp = requests.post(
            self.url + "/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
            } | options
        )

        # raise an error if one occured
        resp.raise_for_status()
        # get the body
        body = resp.json()
        print(body)

        out = LlmResponseSchema(
            model=body['model'],
            response=body['message']['content'],
            think=None,
        )

        if self.thinking and out.response.startswith("<think>"):
            parts = out.response.split("</think>", 1)
            out.think = parts[0].removeprefix("<think>").strip()
            out.response = parts[1].strip()

        return out


class ExpertPrompt(Llm):
    pass


if __name__ == "__main__":
    # llm = Ollama("qwen3:14b")
    llm = Ollama("deepseek-r1:14b", thinking=True)
    print("processing...")

    print(llm.invoke("How are you doing?"))
