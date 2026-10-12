import streamlit as st
import os
import tempfile
from ingest import ingest_pdf
from rag import answer_question

# Configure the Streamlit page
st.set_page_config(
    page_title="StudySphere AI",
    page_icon="📚",
    layout="wide"
)

# Application title
st.title("📚 StudySphere AI")

# Application description
st.write(
    "Your AI-powered PDF assistant. "
    "Upload PDF files and ask questions about their content."
)

# Sidebar
uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:

    st.write("**File name:**", uploaded_file.name)

    st.write(
        "**File size:**",
        f"{uploaded_file.size / 1024:.2f} KB"
    )

    if st.button("Process PDF"):

        with st.spinner("Processing your PDF..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(uploaded_file.getvalue())
                temp_pdf_path = temp_file.name

            try:
                result = ingest_pdf(temp_pdf_path)

                st.session_state["pdf_processed"] = True
                st.session_state["pdf_name"] = uploaded_file.name

                st.success("PDF processed successfully!")

                st.write("**Pages:**", result["pages"])
                st.write("**Chunks:**", result["chunks"])

            except Exception as e:
                st.error(f"Error processing PDF: {e}")

            finally:
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
                    
# Main chat area
st.subheader("💬 Ask Your PDF")

question = st.chat_input("Ask a question about your PDF...")

if question:

    if not st.session_state.get("pdf_processed", False):

        st.warning("Please upload and process a PDF first.")

    else:

        st.chat_message("user").write(question)

        with st.chat_message("assistant"):

            with st.spinner("Searching your PDF and generating an answer..."):

                try:
                    answer, metadata = answer_question(question)

                    st.markdown(answer)

                    # Display sources
                    st.subheader("📚 Sources")

                    displayed_sources = set()

                    for item in metadata:

                        source = item["source"]
                        page = item["page"]

                        if (source, page) not in displayed_sources:

                            st.write(f"📄 **{source}** — Page {page}")

                            displayed_sources.add((source, page))

                except Exception as e:

                    st.error(f"Error generating answer: {e}")