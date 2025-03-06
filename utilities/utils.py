from configurations.config import model, index
from generation.generate_response import generate_response
from storage.store import store_message
from conversation import conversation_history

def is_vector_db_empty():
  """Check if there are any stored messages in the Pinecone index for a given user."""
  results = index.query(vector=[[0] * model.get_sentence_embedding_dimension()], top_k=1, include_metadata=False)

  # If there are no matches, the vector database is empty
  return len(results.get("matches", [])) == 0

def chat(user_id):

  if user_id not in conversation_history:
    conversation_history[user_id] = []
  
  while True:
    query = input("Enter your query (or type 'exit' to quit): ")
    if query.lower() == 'exit':
      print("Exiting chat...")
      break

    print("\nConversation History:")
    for entry in conversation_history[user_id][-10:]: 
        print(entry)
        
    if is_vector_db_empty():
      print("No prior messages stored. Storing your first message...")
      response = generate_response(user_id, query)
      print(f"Generated Response: {response}")
    else:
      response = generate_response(user_id, query)
      print(f"Generated Response: {response}")
    
    conversation_history[user_id].append(f"User: {query}")
    conversation_history[user_id].append(f"LLM: {response}")

    print(f"Conversation History: {conversation_history}")

    store_message(user_id, query)