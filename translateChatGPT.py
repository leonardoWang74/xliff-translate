import requests

from translateWrapper import TranslatorWrapper
import os
import openai
from dotenv import load_dotenv
import time

# src, dest languages should be the name of the language e.g. 'english' for english
# create an .env file with OPENAI_API_KEY=YOUR_API_KEY

# you can get your api key from https://platform.openai.com/account/api-keys -> create secret key
# https://platform.openai.com/docs/api-reference/chat/create
class TranslatorChatGPT(TranslatorWrapper):
    prompt = None
    url = "https://api.openai.com/v1/chat/completions"
    model = "gpt-3.5-turbo"
    headers = None

    def init(self, src, dest):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY")
        }
        self.prompt = f"Translate the following {src} text to {dest}: "

    # response['choices'][0]['message']['content']

    def translate(self, text: str):
        json = {
            "model": self.model,
            "messages": [{"role": "user", "content": self.prompt + text}]
        }
        response = requests.post(self.url, json=json, headers=self.headers)
        response_json = response.json()
        print(response_json)
        return response_json['choices'][0]['message']['content']

    def translate_multiple(self, texts: [str]):
        result = []
        for text in texts:
            result.append(self.translate(text))
            time.sleep(0.5)
        return result
