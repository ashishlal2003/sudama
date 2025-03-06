from sentence_transformers import SentenceTransformer
from pinecone import Pinecone,ServerlessSpec
from py2neo import Graph
from google import genai
import os


model = SentenceTransformer("all-MiniLM-L6-v2")
pinecone_api_key = "pcsk_4Nw6ea_Q3B2vNtvhPtWDH7PDaSSM3N9FAN1VNpcQi7pqRWqZ3x3gzf7Q4CDdcMsZ5iXNdA"
client = Pinecone(api_key=pinecone_api_key)

index_name = "chatbot-memory"

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

graph = Graph("neo4j+sp://58009442.databases.neo4j.io", auth=("neo4j", "CswbHH48VK0PBCOYBO1hAXeo-AMvJixnYmqiHBRkbNo"))

genai_api_key = "AIzaSyCVxacwkdmS8Yy8rcxtOI5x6crazqVZfqI"
client = genai.Client(api_key=genai_api_key)