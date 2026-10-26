import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv


# Connect to ChromaDB
client = chromadb.PersistentClient(path="./vectorstore")

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Retrieve relevant chunks from all uploaded PDFs
def retrieve(query, k=5):

    collection = client.get_collection(name="pdf-collection")

    # Convert the question into an embedding
    query_embedding = model.encode(query)

    # Search across the entire collection
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )
    retrieved_chunks = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]

    return retrieved_chunks, retrieved_metadata


# Generate an answer using Groq
def generate_answer(query, retrieved_chunks, retrieved_metadata):

    # Include source information alongside each chunk
    context_parts = []

    for chunk, metadata in zip(retrieved_chunks, retrieved_metadata):

        source = metadata.get("source", "Unknown PDF")
        page = metadata.get("page", "Unknown")

        context_parts.append(
            f"Source: {source}, Page: {page}\n"
            f"Content: {chunk}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are StudySphere AI, an AI assistant that answers questions
about uploaded study documents.

Instructions:
- Answer using only the provided context.
- If the answer is not available in the context, say you could
  not find it in the uploaded documents.
- Give a clear, student-friendly explanation.
- Do not invent facts that are not supported by the context.

Context:
{context}

Question:
{query}

Answer:
"""

    # Load environment variables
    load_dotenv()

    # Initialize Groq client
    groq_client = Groq()

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# Main function called by Streamlit
def answer_question(query):

    retrieved_chunks, retrieved_metadata = retrieve(query, k=5)

    answer = generate_answer(
        query,
        retrieved_chunks,
        retrieved_metadata
    )

    return answer, retrieved_metadata
