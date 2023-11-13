# llm
Large Language Models tutorial

## Stages
1. **Return everything the user inputs:**
```angular2html
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # return everything that the user enters
    await cl.Message(
        content=f' {message.content}', ).send()
```
2. **Pass the message into the ChatGPT API:**
```angular2html

```