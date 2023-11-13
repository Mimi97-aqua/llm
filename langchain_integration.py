import chainlit as cl
import os
import openai
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

template = """ 
        Question: {question}
        Answer: Let's think step by step
        """


@cl.on_chat_start
def main():
    # Variables to initiate as soon as chainlit UI is deployed
    prompt = PromptTemplate(template=template, input_variables=['question'])
    llm_chain = LLMChain(
        prompt=prompt,
        llm=OpenAI(temperature=1, streaming=True),
        verbose=True
    )

    cl.user_session.set('llm_chain', llm_chain)


@cl.on_message
async def main(message: cl.Message):
    llm_chain = cl.user_session.get('llm_chain')

    result = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    await cl.Message(content=result['text']).send()
