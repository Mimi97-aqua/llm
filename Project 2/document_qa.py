import os
import chainlit as cl
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from chainlit.types import AskFileResponse

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)  # Chunk size = 1000 characters
embeddings = OpenAIEmbeddings()  # Uses Ada2 Model

welcome_message = """
Welcome to the Chainlit PDF QA demo! To get started:
1. Upload a PDF of text file
2. Ask a question about the file
"""


def process_file(file: AskFileResponse):
    import tempfile

    if file.type == 'text/plain':
        Loader = TextLoader
    elif file.type == 'application/pdf':
        Loader = PyPDFLoader

    with tempfile.NamedTemporaryFile() as tempfile:
        tempfile.write(file.content)
        loader = Loader(tempfile.name)
        documents = loader.load()
        docs = text_splitter.split_documents(documents)

        for i, doc in enumerate(docs):
            doc.metadata('source') = f'source_{i}'
        return docs