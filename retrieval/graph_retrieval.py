from extraction.relationship import determine_relationship_llm
from config import graph

def retrieve_graph_context(user_id, query):
    """Retrieve relevant context from the Neo4j graph database, emphasizing relationships."""
    relationship = determine_relationship_llm(query)

    print(f"Relationship understood from the query: {relationship}")

    if relationship == "ASKED_ABOUT":
        relationship = "MENTIONED"

    query = f"""
    MATCH (u:User {{id: "{user_id}"}})-[r:{relationship}]-(q:Query)
    RETURN type(r) AS relationship, q.text AS query_text, labels(q) AS node_labels
    LIMIT 5
    """

    results = graph.run(query).data()

    context = [
        f'Relationship: {record["relationship"]}, Query Text: "{record["query_text"]}", Node Labels: {", ".join(record["node_labels"])}'
        for record in results
    ]

    return context

PREDEFINED_RELATIONSHIPS = [
    "ASKED_ABOUT",
    "WORKING_ON",
    "MENTIONED",
    "INTERACTED_WITH",
    "READ_ABOUT"
]