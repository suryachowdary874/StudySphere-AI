from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os
import hashlib


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
client = chromadb.PersistentClient(path="./vectorstore")

# Get the existing collection
collection = client.get_or_create_collection(
    name="pdf-collection"
)


def calculate_file_hash(pdf_path):
    """Generate a SHA-256 fingerprint for a PDF."""

    sha256 = hashlib.sha256()

    with open(pdf_path, "rb") as pdf_file:
        for block in iter(lambda: pdf_file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def fix_source_filename(old_filename, new_filename):
    results = collection.get(
        where={"source": old_filename},
        include=["metadatas"]
    )

    if not results["ids"]:
        print("No matching chunks found.")
        return

    updated_metadatas = []

    for metadata in results["metadatas"]:
        metadata["source"] = new_filename
        updated_metadatas.append(metadata)

    collection.update(
        ids=results["ids"],
        metadatas=updated_metadatas
    )

    print(f"Updated {len(results['ids'])} chunks.")
    

def ingest_pdf(pdf_path, original_filename=None):

    pdf_name = original_filename or os.path.basename(pdf_path)

    # Identify the PDF by its contents
    file_hash = calculate_file_hash(pdf_path)

    # Check whether this exact PDF version is already stored
    existing = collection.get(
        where={"file_hash": file_hash},
        limit=1,
        include=["metadatas"]
    )


    if existing["ids"]:
        print("DEBUG: Duplicate PDF detected. Skipping ingestion.")

        return {
            "filename": pdf_name,
            "pages": 0,
            "chunks": 0,
            "duplicate": True,
            "message": "This PDF has already been processed."
        }

    reader = PdfReader(pdf_path)

    print("Number of pages:", len(reader.pages))

    chunks = []
    metadatas = []

    # Extract text page by page
    for page_index, page in enumerate(reader.pages):

        text = page.extract_text()

        if not text:
            continue

        page_number = page_index + 1
        paragraphs = text.split("\n")
        current_chunk = ""

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            if len(current_chunk) + len(paragraph) <= 800:
                current_chunk += paragraph + "\n"

            else:

                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                    metadatas.append({
                        "source": pdf_name,
                        "page": page_number,
                        "file_hash": file_hash
                    })

                current_chunk = paragraph + "\n"

        # Save the final chunk from the page
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

            metadatas.append({
                "source": pdf_name,
                "page": page_number,
                "file_hash": file_hash
            })

    if not chunks:
        return {
            "filename": pdf_name,
            "pages": len(reader.pages),
            "chunks": 0,
            "duplicate": False,
            "message": "No extractable text found in this PDF."
        }

    print("Number of chunks:", len(chunks))

    # Generate embeddings
    embeddings = model.encode(chunks)

    print("Number of embeddings:", len(embeddings))
    print("Embedding shape:", embeddings.shape)

    # Create deterministic IDs for every chunk
    ids = [
        hashlib.sha256(
            f"{file_hash}_{index}".encode("utf-8")
        ).hexdigest()
        for index in range(len(chunks))
    ]

    # Add the new document to ChromaDB
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print("Total chunks in ChromaDB:", collection.count())

    return {
        "filename": pdf_name,
        "pages": len(reader.pages),
        "chunks": len(chunks),
        "duplicate": False
    }


if __name__ == "__main__":

    result = ingest_pdf(
        "data/documents/Mid_Exam_Data_Analytics_Text_Mining_Notes.pdf"
    )

    print(result)
