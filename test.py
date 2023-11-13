import chainlit as cl
import os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAPI_KEY')
openai.api_key = api_key


@cl.on_message
async def main(message: cl.Message):
    # return everything that the user enters
    await cl.Message(
        content=f' {message.content}', ).send()
