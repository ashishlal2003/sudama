from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from neo4j import GraphDatabase
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_client = Pinecone(api_key=pinecone_api_key)

index_name = os.getenv("INDEX_NAME")
existing_indexes = [index['name'] for index in pinecone_client.list_indexes()]
if index_name not in existing_indexes:
    pinecone_client.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pinecone_client.Index(index_name)

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

graph = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

genai_api_key = os.getenv("GEMINI_API_KEY")
genai_client = genai.Client(api_key=genai_api_key)