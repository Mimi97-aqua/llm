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