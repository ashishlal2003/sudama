from retrieval.graph_retrieval import retrieve_graph_context
from retrieval.vector_retrieval import retrieve_relevant_messages
from configurations.config import genai_client

def get_past_summary(user_id, query):
    """Retrieve a summary of the user's past interactions."""
    graph_memories = retrieve_graph_context(user_id, query)

    vector_memories = retrieve_relevant_messages(user_id, query)

    combined_memory = "\n".join(graph_memories + vector_memories)

    prompt = f"""
      You are an intelligent AI assistant. Use the provided past memory about the user and generate the summary in 500 tokens.

      Your response is supposed to start directly with the summary and nothing else.

      **All Memories**
      {combined_memory}

      """
    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    print(response.text)
    return response.text