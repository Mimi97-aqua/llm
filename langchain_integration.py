import chainlit as cl
import os
import openai
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI

template = """ 
    Question: {question}
    Answer: Let's think step by step
    """

print(template.format(question='What is 1+1'))
