# LLM
Large Language Models [Tutorial](https://youtu.be/xZDB1naRUlk?si=IxDqmmd35XrimPDJ)

### Project 2

## Stages
1. **Basic Intro to Chroma DB:**
   * Chroma is a vector database.
   ```python
    import chromadb

    chroma_client = chromadb.Client()
    collection_name = 'my_collection'  # Vector Database
    
    # Check if collection exists and create it if it doesn't
    if collection_name not in chroma_client.list_collections():
        chroma_client.create_collection(name=collection_name)
    
    # Get collection
    collection = chroma_client.get_collection(name=collection_name)
    
    # Adding data to the db
    collection.add(
        documents=['My name is Loni', 'My name is not Inol'],
        metadatas=[{'source': 'name is True'}, {'source': 'name is False'}],
        ids=['id1', 'id2']
    )
    
    # Querying the collection (db)
    results = collection.query(
        query_texts=['What is my name?'],  # Question
        n_results=1  # Number of results to output
    )
    
    print(results)
    ```
   * **_Cosine similarity_** is used to measure the similarity between the vectors of the query and the vectors of the documents in the database. Through this, documents are ranked based o similarity and the first result is given (that with the top most similarity.)
   * **_Note:_** In the case where more than 1 result is required, the document with the smallest distance is the one with the top-most similarity.

2. **Building a Document-based Q&A System**
* _**Features:**_
  * Semantic search
  * Pinecone
  * LLM
* **_Process:_**
  * The document gets passed into a text splitter. (Splits into chunks -> a continguous sequence of words/tokens. Process begins with tokenization.)
  * The document is passed into an embedding generator
  * The embeddings are stored in the database
    * **_Note:_** An embedding provides a way to represent and work with complex data in a meanngful way and in a high dimensional space.
  * It is queried and the vector_db finds the closest set of 10 sentences to the query using cosine similarity
  * The 10 sentences alongside the query are wrapped into the Q&A model(eg. GPT-3)
  * We ask the model a question, and it gives us the answer as output

```python
import os
import chainlit as cl
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from chainlit.types import AskFileResponse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI(api_key=api_key)


class MyOpenAIEmbeddings(OpenAIEmbeddings):
    def embed_query(self, query):
        if not isinstance(query, str):
            query = str(query)
        return self.embed_documents([query])[0]


# Split text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)  # Chunk size = 1000 characters
embeddings = MyOpenAIEmbeddings()  # Uses Ada2 Model

welcome_message = """
Welcome to the Chainlit PDF QA demo! To get started:
1. Upload a PDF of text file
2. Ask a question about the file
"""


# Function to process file and split it into chunks
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

        # Print or log the content of the loaded document
        print('Loaded document content:', documents)

        docs = text_splitter.split_documents(documents)

        # Labelling chunks as sources
        for i, doc in enumerate(docs):
            doc.metadata['source'] = f'source_{i}'
        return docs


# Function to retrieve data from embeddings and create a Chroma vector store
def get_docsearch(file: AskFileResponse):
    docs = process_file(file)

    # Save data in user session
    cl.user_session.set('docs', docs)

    # Create unique namespaces for file
    docsearch = Chroma.from_documents(
        docs, embeddings
    )
    return docsearch


# Chain UI User Interaction functionality
# Function to handle start of the chat session
@cl.on_chat_start
async def start():
    # Sending image with local file path
    await cl.Message(content='Welcome! You can now chat with your PDFs').send()

    # File processing and chain initialization
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=['text/plain', 'application/pdf'],
            max_size_mb=20,
            timeout=180
        ).send()

    file = files[0]

    msg = cl.Message(content=f'Processing "{file.name}"...')
    await msg.send()

    # No async implementation in the Pinecone client, fallback to sync
    docsearch = await cl.make_async(get_docsearch)(file)

    # Print or log the content of the processed documents
    docs = cl.user_session.get('docs')
    print('Processed Document Content:', [doc.page_content for doc in docs])

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0, streaming=True),
        chain_type="stuff",
        retriever=docsearch.as_retriever(max_tokens_limit=4097),
    )

    # Let the user know that the system is ready
    msg.content = f"`{file.name}` processed. You can now ask questions!"
    await msg.update()

    cl.user_session.set("chain", chain)


# Function to handle incoming messages and provide responses
@cl.on_message
async def main(message):
    chain = cl.user_session.get("chain")  # type: RetrievalQAWithSourcesChain
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message, callbacks=[cb])

    answer = res["answer"]
    sources = res["sources"].strip()
    source_elements = []

    # Get the documents from the user session
    docs = cl.user_session.get("docs")
    metadatas = [doc.metadata for doc in docs]
    all_sources = [m["source"] for m in metadatas]

    if sources:
        found_sources = []

        # Add the sources to the message
        for source in sources.split(","):
            source_name = source.strip().replace(".", "")
            # Get the index of the source
            try:
                index = all_sources.index(source_name)
            except ValueError:
                continue
            text = docs[index].page_content
            found_sources.append(source_name)
            # Create the text element referenced in the message
            source_elements.append(cl.Text(content=text, name=source_name))

        if found_sources:
            answer += f"\nSources: {', '.join(found_sources)}"
        else:
            answer += "\nNo sources found"

    if cb.has_streamed_final_answer:
        cb.final_stream.elements = source_elements
        await cb.final_stream.update()
    else:
        await cl.Message(content=answer, elements=source_elements).send()
```