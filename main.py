import chainlit as cl
from openai import OpenAI
import os

# os.environ['OPENAI_API_KEY'] = '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'

client = OpenAI(
    api_key= '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'
)


# return everything that the user input
@cl.on_message
async def main(message: str):
    # pass message into chatgpt api
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "assistant",
             "content": "You are a helpful assistant"},
            {"role": "user",
             "content": message},
        ],
        temperature=1,
    )
    await cl.Message(content=response).send()
