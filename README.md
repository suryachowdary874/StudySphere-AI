# 📚 StudySphere AI — RAG-Based PDF Question Answering System

StudySphere AI is an AI-powered study assistant that enables students to upload PDF documents, ask questions about their study materials, and receive context-aware answers generated from the uploaded content.

Built using Retrieval-Augmented Generation (RAG), semantic search, vector embeddings, and Large Language Models (LLMs), the application retrieves relevant information from documents and uses it to generate informative answers with source references.

## 🚀 Live Demo

🔗 **Try StudySphere AI:** https://studysphere-ai-7hjx2uht5zhavjrqie7gv5.streamlit.app/

## ✨ Features

- 📄 **PDF Upload:** Upload study materials and academic notes in PDF format.
- ✂️ **Document Chunking:** Split extracted document text into smaller chunks for efficient retrieval.
- 🧠 **Semantic Embeddings:** Generate vector embeddings using Sentence Transformers.
- 🗄️ **Vector Storage:** Store document chunks and embeddings using ChromaDB.
- 🔍 **Semantic Search:** Retrieve relevant document chunks based on the user's question.
- 🤖 **AI-Powered Answers:** Generate context-aware responses using Groq-hosted LLMs.
- 📑 **Source References:** Display source document names and page numbers for retrieved information.
- 🌐 **Web Deployment:** Access the application through Streamlit Community Cloud.

## 🏗️ System Architecture

```text
                 User
                  |
                  v
          Upload PDF Document
                  |
                  v
           PDF Text Extraction
                  |
                  v
            Text Chunking
                  |
                  v
        Sentence Transformer Model
                  |
                  v
          Generate Embeddings
                  |
                  v
              ChromaDB
                  |
                  |  Document Retrieval
                  |
User Question ---> Query Embedding
                  |
                  v
          Semantic Similarity Search
                  |
                  v
         Retrieve Relevant Chunks
                  |
                  v
       Build Context-Aware Prompt
                  |
                  v
             Groq LLM API
                  |
                  v
          Generate Final Answer
                  |
                  v
        Answer + Source References
