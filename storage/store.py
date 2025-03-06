from configurations.config import model, index, graph
from extraction.relationship import determine_relationship_llm

def store_message(user_id, message):
    """Store a user's message in the Pinecone index."""
    embedding = model.encode(message).tolist()
    index.upsert([
        {
            "id": f"{user_id}_{hash(message)}",
            "values": embedding,
            "metadata": {"text": message}
        }
    ])

    """Store in Neo4j"""
    relationship = determine_relationship_llm(message)
    query = f"""
    MERGE (u:User {{id: "{user_id}"}})
    MERGE (q:Query {{text: "{message}"}})
    MERGE (u)-[:{relationship}]->(q)
    """
    graph.run(query, user_id=user_id, message=message)