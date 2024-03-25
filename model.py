from openai import OpenAI
from dotenv import load_dotenv
import os


class Model:
    def __init__(self, _model: str, _temperature: int = 0) -> None:
        self.model = _model
        self.temperature = _temperature

    def setup(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_response(self, prompt: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            temperature=self.temperature
        )
        response: str = completion.choices[0].message
        return response
