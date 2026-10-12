from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os


def ingest_pdf(pdf_path):

    pdf_name = os.path.basename(pdf_path)

    reader = PdfReader(pdf_path)

    print("Number of pages:", len(reader.pages))

    pages = []
    chunks = []
    metadatas = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    for page_data in pages:

        page_number = page_data["page"]
        text = page_data["text"]

        paragraphs = text.split("\n")

        current_chunk = ""

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            if len(current_chunk) + len(paragraph) <= 800:

                current_chunk += paragraph + "\n"

            else:

                chunks.append(current_chunk.strip())

                metadatas.append({
                    "source": pdf_name,
                    "page": page_number
                })

                current_chunk = paragraph + "\n"

        if current_chunk:

            chunks.append(current_chunk.strip())

            metadatas.append({
                "source": pdf_name,
                "page": page_number
            })

    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3]):
        print(f"\n--- chunk {i+1} ---")
        print(chunk)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(chunks)

    print("No. of embeddings:", len(embeddings))
    print("Shape of embeddings:", embeddings.shape)

    client = chromadb.PersistentClient(path="./vectorstore")

    try:
        client.delete_collection(name="pdf-collection")
    except Exception:
        pass

    collection = client.create_collection(name="pdf-collection")

    print("ChromaDB collection created:", collection.name)

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print("Total documents in ChromaDB:", collection.count())

    return {
        "filename": pdf_name,
        "pages": len(reader.pages),
        "chunks": len(chunks)
    }


if __name__ == "__main__":

    result = ingest_pdf(
        "data/documents/Mid_Exam_Data_Analytics_Text_Mining_Notes.pdf"
    )

    print(result)