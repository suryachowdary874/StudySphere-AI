import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv


# Connect to ChromaDB
client = chromadb.PersistentClient(path="./vectorstore")

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Retrieve relevant chunks from ChromaDB
# Retrieve relevant chunks from ChromaDB
def retrieve(query, k=3):

    # Get the current collection from ChromaDB
    collection = client.get_collection(name="pdf-collection")

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )

    retrieved_chunks = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]

    return retrieved_chunks, retrieved_metadata


# Generate an answer using Groq
def generate_answer(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    Answer the question using only the provided context.
    If the answer is not available in the context, say that you
    could not find the answer in the uploaded PDF.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    load_dotenv()

    client = Groq()

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer


# Main function to call from Streamlit
def answer_question(query):

    retrieved_chunks, retrieved_metadata = retrieve(query, k=3)

    answer = generate_answer(query, retrieved_chunks)

    return answer, retrieved_metadata