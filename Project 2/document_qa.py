import os
import chainlit as cl
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from chainlit.types import AskFileResponse

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embeddings = OpenAIEmbeddings()

welcome_message = """
Welcome to the Chainlit PDF QA demo! To get started:
1. Upload a PDF of text file
2. Ask a question about the file
"""