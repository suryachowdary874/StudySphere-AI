import streamlit as st
import os
import tempfile

from ingest import ingest_pdf
from rag import answer_question


# 1. Configure Streamlit

st.set_page_config(
    page_title="StudySphere AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudySphere AI")

st.write(
    "Your AI-powered PDF assistant. "
    "Upload multiple PDF files and ask questions about their content."
)

# 2. Initialize session state

if "processed_pdfs" not in st.session_state:
    st.session_state["processed_pdfs"] = []

if "pdf_processed" not in st.session_state:
    st.session_state["pdf_processed"] = False

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 3. Sidebar: Upload PDFs

st.sidebar.header("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Choose PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    st.write(f"**Selected PDFs:** {len(uploaded_files)}")

    for uploaded_file in uploaded_files:
        st.write(
            f"📄 {uploaded_file.name} "
            f"({uploaded_file.size / 1024:.2f} KB)"
        )

    if st.button("Process PDFs"):

        processed_files = []
        duplicate_files = []
        failed_files = []

        progress_bar = st.progress(0)

        for index, uploaded_file in enumerate(uploaded_files):

            temp_pdf_path = None

            try:

                with st.spinner(
                    f"Processing {uploaded_file.name}..."
                ):

                    # Save the PDF temporarily
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            uploaded_file.getvalue()
                        )

                        temp_pdf_path = temp_file.name

                    # Process the PDF
                    result = ingest_pdf(
                        temp_pdf_path,
                        original_filename=uploaded_file.name
                    )

                    # Check whether it is a duplicate
                    if result.get("duplicate", False):

                        duplicate_files.append(
                            uploaded_file.name
                        )

                    # Check whether processing succeeded
                    elif result.get("chunks", 0) > 0:

                        processed_files.append(result)

                    else:

                        failed_files.append(
                            f"{uploaded_file.name}: "
                            f"{result.get('message', 'No extractable text found.')}"
                        )

            except Exception as e:

                failed_files.append(
                    f"{uploaded_file.name}: {str(e)}"
                )

            finally:

                if (
                    temp_pdf_path
                    and os.path.exists(temp_pdf_path)
                ):
                    os.remove(temp_pdf_path)

            progress_bar.progress(
                (index + 1) / len(uploaded_files)
            )

        progress_bar.empty()

        # Display successful processing results
        if processed_files:

            for result in processed_files:

                filename = result["filename"]

                if filename not in st.session_state["processed_pdfs"]:
                    st.session_state["processed_pdfs"].append(
                        filename
                    )

            st.session_state["pdf_processed"] = True

            st.success(
                f"✅ Successfully processed "
                f"{len(processed_files)} new PDF(s)!"
            )

            for result in processed_files:

                st.write(f"📄 **{result['filename']}**")
                st.write(f"Pages: {result['pages']}")
                st.write(f"Chunks: {result['chunks']}")

        # Display duplicate notifications
        for filename in duplicate_files:

            st.warning(
                f"📄 **{filename}** has already been processed! "
                "You can ask questions about this PDF without "
                "uploading it again."
            )

        # Display genuine errors only
        if failed_files:

            st.error("Some PDFs could not be processed:")

            for error in failed_files:
                st.write(f"⚠️ {error}")

        # Allow questions if new or duplicate PDFs were selected
        if processed_files or duplicate_files:
            st.session_state["pdf_processed"] = True

# 4. Sidebar: Processed documents

processed_pdfs = st.session_state["processed_pdfs"]

if processed_pdfs:

    st.sidebar.subheader("✅ Processed Documents")

    for pdf_name in processed_pdfs:
        st.sidebar.write(f"📄 {pdf_name}")

# 5. Chat history controls

st.subheader("💬 Ask Your PDFs")

col1, col2 = st.columns([5, 1])

with col1:
    st.caption(
        f"Conversation messages: "
        f"{len(st.session_state['chat_history'])}"
    )

with col2:

    if st.button("🗑️ Clear Chat"):

        st.session_state["chat_history"] = []
        st.rerun()

# 6. Display previous conversations

for chat in st.session_state["chat_history"]:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):

        st.markdown(chat["answer"])

        sources = chat.get("sources", [])

        if sources:

            with st.expander("📚 Sources"):

                for source in sources:

                    st.write(
                        f"📄 **{source['source']}** — "
                        f"Page {source['page']}"
                    )


# 7. Accept a new question

question = st.chat_input(
    "Ask a question about your uploaded PDFs..."
)


if question:

    if not st.session_state["pdf_processed"]:

        st.warning(
            "Please upload and process at least one PDF first."
        )

    else:

        # Display the new question
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching your PDFs and generating an answer..."
            ):

                try:

                    answer, metadata = answer_question(question)

                    st.markdown(answer)

                    # Collect unique source references
                    sources = []
                    displayed_sources = set()

                    for item in metadata:

                        source_name = item.get(
                            "source", "Unknown PDF"
                        )

                        page_number = item.get(
                            "page", "Unknown"
                        )

                        source_key = (
                            source_name,
                            page_number
                        )

                        if source_key not in displayed_sources:

                            sources.append({
                                "source": source_name,
                                "page": page_number
                            })

                            displayed_sources.add(source_key)

                    # Display sources for this answer
                    if sources:

                        with st.expander("📚 Sources"):

                            for source in sources:

                                st.write(
                                    f"📄 **{source['source']}** — "
                                    f"Page {source['page']}"
                                )

                    # Save the conversation
                    st.session_state["chat_history"].append({
                        "question": question,
                        "answer": answer,
                        "sources": sources
                    })

                except Exception as e:

                    st.error(
                        f"Error generating answer: {e}"
                    )