from configurations.config import model, index, graph
from extraction.relationship import determine_relationship_llm
from configurations.config import graph 

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
    cypher_query = f"""
    MERGE (u:User {{id: "{user_id}"}})
    MERGE (q:Query {{text: "{message}"}})
    MERGE (u)-[:{relationship}]->(q)
    """

    with graph.session() as session:
        results = session.run(cypher_query, user_id=user_id, message=message).data()

    return results