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
