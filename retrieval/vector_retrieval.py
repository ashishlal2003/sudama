from configurations.config import model, index

def retrieve_relevant_messages(user_id, query, top_k=5, min_score=0.5):
    """Retrieve relevant messages from the Pinecone index based on a query."""
    query_embedding = model.encode(query).tolist()
    results = index.query(vector=[query_embedding], top_k=top_k, include_metadata=True)
    relevant_texts = [
        res["metadata"]["text"]
        for res in results["matches"]
        if res["score"] > min_score
    ]
    return relevant_texts