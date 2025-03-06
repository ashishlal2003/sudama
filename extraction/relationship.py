from configurations.config import client
from extraction.predefined_relationships import PREDEFINED_RELATIONSHIPS

def determine_relationship_llm(user_query):
    prompt = f"""
    Given the following user query: "{user_query}", classify the relationship between the user and the mentioned topics/entities using one of the following predefined relationship types:

    - ASKED_ABOUT
    - WORKING_ON
    - MENTIONED
    - INTERACTED_WITH
    - READ_ABOUT

    Respond with only the relationship name.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    relationship = response.text.strip()

    # Validate the LLM's response
    if relationship not in PREDEFINED_RELATIONSHIPS:
        relationship = "MENTIONED"  # Default to a general category

    return relationship