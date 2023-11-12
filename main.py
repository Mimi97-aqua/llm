import chainlit as cl
import openai
import os

os.environ['OPENAI_API_KEY'] = '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'

# return everything that the user input


@cl.on_message
async def main(message : str):
    await cl.Message(content = message).send()