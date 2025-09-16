import requests
from abc import ABC, abstractmethod


class Llm(ABC):
    @abstractmethod
    def invoke(self, prompt: str, system: str = None):
        raise NotImplementedError()


class Ollama(Llm):
    def __init__(self, model, thinking=False):
        self.url = "http://localhost:11434/api"
        self.model = model
        self.thinking = thinking

    def invoke(self, prompt: str, system: str = None):
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
            }
        )

        # raise an error if one occured
        resp.raise_for_status()
        # get the body
        body = resp.json()

        return body


class ExpertPrompt(Llm):
    pass


if __name__ == "__main__":
    # llm = Ollama("qwen3:14b")
    llm = Ollama("deepseek-r1:14b")
    print("processing...")

    print(llm.invoke("How are you doing?"))
