# llm
Large Language Models tutorial

## Stages
1. **Return everything the user inputs:**
```angular2html
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # return everything that the user enters
    await cl.Message(
        content=f' {message.content}', ).send()
```
2. **Pass the message into the ChatGPT API:**
```angular2html
import chainlit as cl
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)  # Instantiating OpenAI client with API Key


@cl.on_message
async def main(message: cl.Message):
    # pass the message into the chatgpt api
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        temperature=1,
        messages=[
            {'role': 'assistant', 'content': 'You are a helpful assistant'},
            {'role': 'user', 'content': message.content}
        ]
    )

    # return everything that the user enters
    await cl.Message(content=f"{response.choices[0].message.content}").send()
```