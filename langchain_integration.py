import chainlit as cl
import os
import openai
from openai import OpenAI
from langchain import PromptTemplate, OpenAI, LLMChain

template = """ 
    Question: {question}
    Answer: Let's think step by step
    """
