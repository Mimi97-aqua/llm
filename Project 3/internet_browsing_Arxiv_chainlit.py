from langchain import OpenAI, LLMMathChain, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from openai import OpenAI
from dotenv import load_dotenv
import os
import chainlit as cl
import time

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI(api_key=api_key)


@cl.on_chat_start
def start():
    llm = ChatOpenAI(temperature=0.5, streaming=True)
    tools = load_tools(
        ["arxiv"]
    )

    agent_chain = initialize_agent(
        tools,
        llm,
        max_iterations=10,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    cl.user_session.set("agent", agent_chain)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    while True:
        try:
            await cl.make_async(agent.run)(message, callbacks=[cb])
            break  # Break out of the loop if the request is successful
        except cl.OpenAIError as e:
            if e.code == 'rate_limit_exceeded':
                # If rate limit exceeded, wait for 20 seconds and retry
                print("Rate limit exceeded. Waiting for 20 seconds...")
                time.sleep(20)
            else:
                # Handle other OpenAI errors
                print(f"OpenAI Error: {e}")
                break
