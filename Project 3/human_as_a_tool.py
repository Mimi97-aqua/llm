from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType
from dotenv import load_dotenv
from openai import OpenAI
import os
import openai

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI(api_key=api_key)

llm = ChatOpenAI(temperature=0.5)
math_llm = OpenAI(temperature=0.5)
tools = load_tools(
    ['human', 'llm-math'],
    llm=math_llm
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent_chain.run("what is my math problem and its solution")