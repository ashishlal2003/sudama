from sentence_transformers import SentenceTransformer
from pinecone import Pinecone,ServerlessSpec
from py2neo import Graph
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))
pinecone_api_key = os.getenv("PINECONE_API_KEY")
client = Pinecone(api_key=pinecone_api_key)

index_name = os.getenv("INDEX_NAME")

existing_indexes = [index['name'] for index in client.list_indexes()]
if index_name not in existing_indexes:
  client.create_index(
      name=index_name,
      dimension=384,
      metric="cosine",
      spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
  )

index = client.Index(index_name)

graph = Graph(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))

genai_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=genai_api_key)