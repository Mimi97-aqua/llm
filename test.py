import chainlit as cl
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAPI_KEY')


@cl.on_message
async def main(message: cl.Message):
    # return everything that the user enters
    await cl.Message(
        content=f' {message.content}', ).send()
