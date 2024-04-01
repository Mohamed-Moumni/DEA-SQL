"""
Module: openai_wrapper.py

This module provides a wrapper class `Model` for interacting with the OpenAI API.

Usage:
    Initialize the Model object with the desired model name and optionally temperature.
    Call the `setup()` method to set up the OpenAI client using the API key from the environment variables.
    Use the `generate_response()` method to generate a response based on the provided prompt.

Example:
    from openai_wrapper import Model

    # Initialize Model object
    model = Model(_model="text-davinci-002")

    # Set up OpenAI client
    model.setup()

    # Generate response based on prompt
    prompt = "What is the capital of France?"
    response = model.generate_response(prompt)
    print(response)

Attributes:
    model (str): The name of the OpenAI model to use.
    temperature (int): The temperature parameter for response generation.
    client: The OpenAI client object for interacting with the API.

Methods:
    __init__(self, _model: str, _temperature: int = 0) -> None:
        Initializes the Model object with the provided model name and temperature.

    setup(self):
        Sets up the OpenAI client using the API key from the environment variables.

    generate_response(self, prompt: str) -> str:
        Generates a response based on the provided prompt using the initialized model.

"""

from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List

class Model:
    def __init__(self, _model: str, _temperature: int = 0) -> None:
        self.model = _model
        self.temperature = _temperature

    def setup(self):
        """
        Sets up the OpenAI client using the API key from the environment variables.
        """
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response based on the provided prompt using the initialized model.

        Args:
            prompt (str): The prompt to generate the response.

        Returns:
            str: The generated response.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            temperature=self.temperature,
        )
        response: str = completion.choices[0].message
        return response
