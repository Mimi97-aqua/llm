# LLM
Large Language Models [Tutorial](https://youtu.be/xZDB1naRUlk?si=IxDqmmd35XrimPDJ)

### Project 3
GPT Researcher

**_Tools:_**
* Arxiv
* Human as a tool: Correcting your model when it makes a mistakes by talking to it rather than changing your parameters.

## Stages
1. **Getting Started with Language Understanding Tools (Arxiv):**
```python
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI(api_key=api_key)

llm = ChatOpenAI(temperature=0.3)
tools = load_tools(
    ['arxiv']
)

agent_chain = initialize_agent(
    tools,
    llm,
    max_iterations=5,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Algorithm for LLM
    verbose=True,
    handle_parsing_errors=True
)

agent_chain.run(
    'What is RLHF?'
)
```
2. **Integrating Arxiv with ChainLit:**
```python
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
    tools = load_tools(["arxiv"])

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

    # Get user input/prompt
    user_question = message.content

    action = 'arxiv'
    action_input = user_question
    observation = "I'm interested in getting more information about it."

    while True:
        try:
            # Ensure message follow expected format
            formatted_message = (f"Action: {action},"
                                 f"Action Input: {action_input},"
                                 f" Observation: {observation}")

            # Using formatted message API request
            await cl.make_async(agent.run)(formatted_message, callbacks=[cb])
            break  # Break out of the loop if the request is successful
        except cl.OpenAIError as e:
            if e.code == 'rate_limit_exceeded':
                # If rate limit exceeded, wait for 20 seconds and retry
                print("Rate limit exceeded. Waiting for 20 seconds...")
                time.sleep(20)
            else:
                # Print the error details
                print(f"OpenAI Error: {e}")
                print(f"Error message: {e.message}")
                print(f"Error code: {e.code}")
                print(f"Error type: {e.type}")
                print(f"Error param: {e.param}")
                break
```
3. **Human as a tool example with llm_math:**
```python
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(temperature=0.5)
math_llm = OpenAI(temperature=0.5)
tools = load_tools(
    ["human", "llm-math"],
    llm=math_llm,
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent_chain.run("what is my math problem and its solution")
```