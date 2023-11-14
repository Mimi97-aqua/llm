# LLM
Large Language Models [Tutorial](https://youtu.be/xZDB1naRUlk?si=IxDqmmd35XrimPDJ)

### Project 1

## Stages
1. **Return everything the user inputs:**
```python
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # return everything that the user enters
    await cl.Message(
        content=f' {message.content}', ).send()
```
2. **Pass the message into the ChatGPT API (Chat Completion):**
```python
import chainlit as cl
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)  # Instantiating OpenAI client with API Key


@cl.on_message
async def main(message: cl.Message):
    # pass the message into the chatgpt api
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        temperature=1,
        messages=[
            {'role': 'assistant', 'content': 'You are a helpful assistant'},
            {'role': 'user', 'content': message.content}
        ]
    )

    # return everything that the user enters
    await cl.Message(content=f"{response.choices[0].message.content}").send()
```
3. **LangChain Integration:**
   * _**Test Integration using PromptTemplate:**_
   ```python
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
    ```
   * **_LangChain Integration with OpenAI:_**
   ```python
   import chainlit as cl
   import os
   from openai import OpenAI
   from langchain.prompts import PromptTemplate
   from langchain.chains import LLMChain
   from langchain.llms.openai import OpenAI
   from dotenv import load_dotenv
   
   load_dotenv()
   api_key = os.getenv('OPENAI_API_KEY')
   
   template = """ 
           Question: {question}
           Answer: {answer}
           """
   
   
   @cl.on_chat_start
   def main():
       # Variables to initiate as soon as chainlit UI is deployed
       prompt = PromptTemplate(template=template, input_variables=['question', 'answer'])
       llm_chain = LLMChain(
           prompt=prompt,
           llm=OpenAI(api_key=api_key, temperature=1, streaming=True),
           verbose=True
       )

    cl.user_session.set('llm_chain', llm_chain)


   @cl.on_message
   async def main_1(message: cl.Message):
       llm_chain = cl.user_session.get('llm_chain')

    # Initial answer
    answer = ''

    # Processing user's input
    result = await llm_chain.acall({'question': message.content, 'answer': ''}, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Get generated answer from result
    if 'text' in result:
        answer = result['text']

    # Send respond back to user
    await cl.Message(content=answer).send()
   ```