# 📚 StudySphere AI

StudySphere AI is an AI-powered study assistant that allows students to upload their study material, ask questions, and receive context-aware answers grounded in the uploaded document.

The application uses a RAG-style (Retrieval-Augmented Generation) pipeline to retrieve relevant information from study material and uses a Large Language Model through the Groq API to generate clear, student-friendly answers.

---

## 🚀 Features

- 📄 Upload personal study notes
- 💬 Ask questions directly from uploaded documents
- ✂️ Automatic text chunking with overlapping chunks
- 🔍 Retrieval of relevant context from study material
- 🤖 AI-powered answer generation using Groq LLM
- 🎯 Answers grounded in the uploaded document
- 🔎 View the retrieved context used to generate an answer
- 🔐 Secure API key management using Streamlit Secrets
- 🌐 Interactive web interface built with Streamlit
- ☁️ Deployed as a publicly accessible web application

---

## 🧠 How It Works

The current StudySphere AI pipeline follows this workflow:

User Uploads Study Notes
        ↓
Text Extraction
        ↓
Text Chunking
        ↓
Keyword-Based Retrieval
        ↓
Most Relevant Chunk
        ↓
Prompt Construction
        ↓
Groq LLM
        ↓
Context-Grounded Answer

The uploaded document is divided into overlapping chunks. When a user asks a question, the system compares keywords from the question with each chunk and retrieves the most relevant context.

The retrieved context and the user's question are then provided to the LLM, which generates an answer based on the available study material.

---

## 🛠️ Tech Stack

- **Python** — Core programming language
- **Streamlit** — Web application interface
- **Groq API** — Fast LLM inference
- **Llama 3.3 70B Versatile** — Large Language Model
- **RAG-style Retrieval** — Context retrieval and grounded generation
- **Text Chunking** — Document segmentation with overlapping chunks
- **Keyword Matching** — Current retrieval mechanism

---

## 📊 Evaluation Framework

A structured evaluation framework is planned to measure both retrieval quality and answer generation quality.

### RAGAS

RAGAS will be used to evaluate the overall RAG pipeline using metrics related to:

- Faithfulness
- Answer relevancy
- Context relevance
- Context recall

### RAGChecker

RAGChecker is planned for fine-grained analysis of the RAG pipeline to identify whether errors originate from:

- Document retrieval
- Context selection
- Answer generation

### Custom Evaluation Metrics

StudySphere AI will also include application-specific metrics such as:

- Retrieval Hit Rate
- Context Relevance
- Answer Groundedness
- Response Time
- Retrieval Accuracy

These evaluations will help identify weaknesses in the RAG pipeline and guide future improvements.

---

## 🔮 Future Enhancements

The current keyword-based retrieval system will be upgraded into a semantic RAG architecture.

Planned architecture:

Document Upload (PDF / TXT)
        ↓
Text Extraction
        ↓
Text Chunking
        ↓
Sentence Transformer Embeddings
        ↓
FAISS Vector Database
        ↓
User Question
        ↓
Query Embedding
        ↓
Semantic Similarity Search
        ↓
Top-K Relevant Chunks
        ↓
Groq LLM
        ↓
Grounded Answer
        ↓
RAG Evaluation

Future improvements include:

- 📑 PDF document support
- 🧠 Sentence Transformer embeddings
- 🔎 Semantic search instead of keyword matching
- 🗄️ FAISS vector database integration
- 📚 Multiple-document support
- 🎯 Top-K context retrieval
- 🔗 Source citations for generated answers
- 📊 RAGAS-based evaluation
- 🔬 RAGChecker-based pipeline analysis
- 📈 Custom RAG evaluation dashboard

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd studysphere-ai
