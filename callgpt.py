import openai
from config import OPENAPI_ID, STORY_PROMPT
import os


class GPT:
    def __init__(self):
        openai.api_key = OPENAPI_ID
        self.model = "gpt-4"
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)

    def call_gpt(self):
        res = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        return res.choices[0].message.content
    

if __name__ == "__main__":
    gpt = GPT()
    gpt.add_message({"role": "user", "content": STORY_PROMPT})
    print(gpt.call_gpt())
