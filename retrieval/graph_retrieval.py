from extraction.relationship import determine_relationship_llm
from configurations.config import graph 

def retrieve_graph_context(user_id, query):
    """Retrieve relevant context from the Neo4j graph database, emphasizing relationships."""
    relationship = determine_relationship_llm(query)

    print(f"Relationship understood from the query: {relationship}")

    if relationship == "ASKED_ABOUT":
        relationship = "MENTIONED"

    valid_relationships = {"MENTIONED", "WORKING_ON", "INTERACTED_WITH", "READ_ABOUT"}
    if relationship not in valid_relationships:
        raise ValueError(f"Invalid relationship type: {relationship}")

    cypher_query = f"""
    MATCH (u:User {{id: $user_id}})-[r:{relationship}]-(q:Query)
    RETURN type(r) AS relationship, q.text AS query_text, labels(q) AS node_labels
    LIMIT 5
    """

    with graph.session() as session:
        results = session.run(cypher_query, user_id=user_id).data()

    context = [
        f'Relationship: {record["relationship"]}, Query Text: "{record["query_text"]}", Node Labels: {", ".join(record["node_labels"])}'
        for record in results
    ]

    return context
