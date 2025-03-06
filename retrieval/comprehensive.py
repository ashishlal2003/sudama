from datetime import datetime, timedelta
from config import graph
from extraction.entities import extract_entities
from extraction.intent import extract_intent
from retrieval.vector_retrieval import retrieve_relevant_messages
from retrieval.graph_retrieval import retrieve_graph_context

def retrieve_comprehensive_context(user_id, query):
    """
    Retrieve comprehensive context from both vector and graph databases,
    organized by different context types.

    Args:
        user_id: ID of the user
        query: Current user query

    Returns:
        Dictionary containing various context types
    """
    # Extract entities and intent from the query
    entities = extract_entities(query)
    intent = extract_intent(query)

    # Retrieve contexts from vector and graph databases
    vector_contexts = retrieve_relevant_messages(user_id, query)
    graph_contexts = retrieve_graph_context(user_id, query)

    # Get entity-specific context
    entity_context = []
    for entity in entities:
      # Extract the entity name by splitting "name (type)"
      entity_name = entity.split(" (")[0]  # Extracts "John Doe" from "John Doe (PERSON)"
      
      results = graph.run(f"""
      MATCH (u:User {{id: '{user_id}'}})-[:ASKED]->(q:Query)-[:MENTIONS]->(e:Entity {{name: '{entity_name}'}})
      RETURN q.text as query_text, q.timestamp as timestamp
      ORDER BY q.timestamp DESC
      LIMIT 3
      """).data()

      for res in results:
          entity_context.append(f"Previously mentioned {entity_name} in: \"{res['query_text']}\" at {res['timestamp']}")


    # Get recent conversation context
    recent_context = graph.run(f"""
    MATCH (u:User {{id: '{user_id}'}})-[:ASKED]->(q:Query)-[:HAS_RESPONSE]->(r:Response)
    WHERE q.timestamp > '{(datetime.now() - timedelta(hours=24)).isoformat()}'
    RETURN q.text as query, r.text as response, q.timestamp as timestamp
    ORDER BY q.timestamp DESC
    LIMIT 5
    """).data()

    recent_exchanges = [f"User asked: \"{res['query']}\" and received: \"{res['response']}\"" for res in recent_context]

    return {
        "vector_contexts": vector_contexts,
        "graph_contexts": graph_contexts,
        "entity_contexts": entity_context,
        "recent_exchanges": recent_exchanges,
        "detected_entities": entities,
        "detected_intent": intent
    }