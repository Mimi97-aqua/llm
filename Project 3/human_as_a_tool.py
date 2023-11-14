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
