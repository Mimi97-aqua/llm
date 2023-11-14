import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.Collection(name='my_collection')  # Vector Database

# Adding data to the db
collection.add(
    documents=['My name is Loni', 'My name is not Inol'],
    metadata=[{'source': 'name is True'}, {'source': 'name is False'}],
    ids=['id1', 'id2']
)