📚 StudySphere AI

StudySphere AI is an AI-powered study assistant that allows students to upload their study material, ask questions, and receive context-aware answers grounded in the uploaded document.

The application uses a semantic RAG (Retrieval-Augmented Generation) pipeline — sentence embeddings and cosine similarity search — to retrieve relevant information from study material, then uses a Large Language Model through the Groq API to generate clear, student-friendly answers.

🚀 Features

* 📄 Upload personal study notes
* 💬 Ask questions directly from uploaded documents
* ✂️ Automatic text chunking with overlapping chunks
* 🧠 Semantic retrieval using sentence embeddings (not keyword matching)
* 🔍 Cosine similarity search to find the most relevant chunks
* 🎯 Top-K retrieval — combines the top 3 most relevant excerpts as context
* 🤖 AI-powered answer generation using Groq LLM
* 🎯 Answers grounded in the uploaded document
* 🔎 View the retrieved context (with similarity scores) used to generate an answer
* 🔐 Secure API key management using Streamlit Secrets
* 🌐 Interactive web interface built with Streamlit

🧠 How It Works

The StudySphere AI pipeline follows this workflow:

```
User Uploads Study Notes
        ↓
   Text Extraction
        ↓
   Text Chunking (overlapping chunks)
        ↓
Sentence Transformer Embeddings (per chunk)
        ↓
   In-Memory Vector Store
        ↓
     User Question
        ↓
   Query Embedding (same model as chunks)
        ↓
Cosine Similarity Search
        ↓
   Top-K Relevant Chunks
        ↓
   Prompt Construction
        ↓
       Groq LLM
        ↓
Context-Grounded Answer
```

The uploaded document is split into overlapping chunks, and each chunk is converted into a numerical embedding using a Sentence Transformer model (`all-MiniLM-L6-v2`), run locally.

When a user asks a question, the question is embedded using the same model, and compared against every chunk's embedding using cosine similarity. The top 3 most semantically relevant chunks are retrieved — this means the system matches based on **meaning**, not just exact keyword overlap, so a question can match relevant content even when it's phrased differently from the source text.

The retrieved chunks and the user's question are then combined into a single prompt and passed to the LLM, which generates an answer grounded only in that retrieved context.

🛠️ Tech Stack

* Python — Core programming language
* Streamlit — Web application interface
* Groq API — Fast LLM inference
* Llama 3.3 70B Versatile — Large Language Model
* Sentence Transformers (`all-MiniLM-L6-v2`) — Local embedding model for semantic retrieval
* NumPy — Cosine similarity computation
* Semantic RAG — Embedding-based retrieval and grounded generation
* Text Chunking — Document segmentation with overlapping chunks

🔮 Future Enhancements

Planned improvements to further strengthen the retrieval pipeline:

* 📑 PDF document support (currently TXT only)
* 🗄️ FAISS / dedicated vector database integration for larger documents
* 📚 Multiple-document support
* 🔀 Hybrid search — combining semantic search with keyword (BM25) matching for exact terms
* 🏆 Reranking with a cross-encoder for more precise top-K selection
* ✍️ Query rewriting to handle vague or poorly-phrased questions
* 🔗 Source citations for generated answers
* 📊 RAGAS-based evaluation
* 🔬 RAGChecker-based pipeline analysis
* 📈 Custom RAG evaluation dashboard

⚙️ Installation

Clone the repository:

```
git clone <your-repository-url>
cd studysphere-ai
```
