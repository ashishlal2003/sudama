from config import client
from retrieval.graph_retrieval import retrieve_graph_context
from retrieval.vector_retrieval import retrieve_relevant_messages
from conversation import conversation_history

def generate_response(user_id, query):
    """Generate a response using GraphDB, VectorDB, and LLM context refinement."""

    graph_memories = retrieve_graph_context(user_id, query)

    vector_memories = retrieve_relevant_messages(user_id, query)

    history = "\n".join(conversation_history[user_id][-10:]) if user_id in conversation_history else "No previous conversation history."

    prompt = f"""
      You are an intelligent AI assistant. Use the provided user memory to generate a relevant response.

      **User Query:**
      {query}

      **Previously Asked Similar Questions:**
      {vector_memories if vector_memories else "None found."}

      **Relevant Knowledge Graph Relationships:**
      {graph_memories if graph_memories else "None found."}

      **Most Recent Conversation History:**
      {history}

      **Instructions:**
      - If relevant past queries or relationships exist, use them to improve the response.
      - If no relevant memory is found, answer based on general knowledge.
      - Keep the response concise, clear, and directly relevant to the query.

      **Final Response:**
    """


    print(f"\nVector Memories:{vector_memories}")
    print(f"\nGraph Memories: {graph_memories}")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text
