from configurations.config import genai_client
from extraction.get_past_summary import get_past_summary
from conversation import conversation_history

def generate_response(user_id, query):
    """Generate a response using GraphDB, VectorDB, and LLM context refinement."""

    print(f"Past summarized: {get_past_summary(user_id, query)}")

    summary = get_past_summary(user_id, query)
    # history = "\n".join(conversation_history[user_id][-10:]) if user_id in conversation_history else "No previous conversation history."
    history = "\n".join(f"User: {q}\nLLM: {r}" for q, r in conversation_history[user_id][-10:])
    prompt = f"""
    User Query: {query}
    Past Memory: {summary if summary else "None found."}
    Recent Conversation History: {history}

    Generate a concise and context-aware response.
    """


    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text