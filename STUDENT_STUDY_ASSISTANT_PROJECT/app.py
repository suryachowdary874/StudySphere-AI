import streamlit as st
from groq import Groq

# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------
st.set_page_config(
    page_title="StudySphere AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #080d20;
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111b40;
        border-right: 1px solid #2b3c78;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        font-size: 1rem;
        color: #e7ecff;
        line-height: 1.7;
    }

    /* Main brand name — centered on main page */
    .main-brand {
        text-align: center;
        font-size: 3.8rem;
        font-weight: 900;
        color: white;
        margin-top: 30px;
        margin-bottom: 30px;
        letter-spacing: -1px;
    }

    /* Hero box */
    .hero {
        background: linear-gradient(100deg, #29478e, #512d7e);
        border: 1px solid #627ad3;
        border-radius: 22px;
        padding: 42px 38px;
        margin: 10px 0 30px 0;
    }

    .hero h1 {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: white;
        margin-bottom: 15px;
    }

    .hero p {
        text-align: center;
        font-size: 1.3rem;
        color: #e4e9ff;
        margin: 0;
    }

    /* Section headings */
    .section-title {
        font-size: 1.55rem;
        font-weight: 750;
        color: #f3f5ff;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Feature cards */
    .feature-card {
        background-color: #17234d;
        border: 1px solid #334d99;
        border-radius: 18px;
        padding: 24px;
        min-height: 145px;
        margin-bottom: 18px;
    }

    .feature-card h3 {
        font-size: 1.22rem;
        color: white;
        margin-top: 0;
        margin-bottom: 16px;
    }

    .feature-card p {
        font-size: 1rem;
        color: #d5ddff;
        line-height: 1.65;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #252735;
        border-radius: 12px;
        padding: 10px;
    }

    /* Question box */
    textarea {
        font-size: 1.1rem !important;
        background-color: #252735 !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* Generate button */
    .stButton > button {
        width: 100%;
        background-color: #ff4d55;
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 14px;
    }

    .stButton > button:hover {
        background-color: #e83e47;
        color: white;
    }

    /* Answer box */
    .answer-box {
        background-color: #17234d;
        border-left: 5px solid #7c95ff;
        border-radius: 12px;
        padding: 25px;
        font-size: 1.1rem;
        line-height: 1.8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# DOCUMENT PROCESSING FUNCTIONS
# ---------------------------------------------------
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))

    return chunks


def clean_word(word):
    return word.lower().strip(".,!?;:()[]{}\"'")


def get_keywords(text):
    words = text.split()
    keywords = set()

    for word in words:
        cleaned = clean_word(word)

        if len(cleaned) >= 4:
            keywords.add(cleaned)

    return keywords


def score_chunk(chunk, question_keywords):
    chunk_keywords = get_keywords(chunk)
    common_words = chunk_keywords.intersection(question_keywords)

    return len(common_words)


def get_best_chunk(chunks, question, min_score=1):
    question_keywords = get_keywords(question)

    best_chunk = None
    best_score = -1

    for chunk in chunks:
        score = score_chunk(chunk, question_keywords)

        if score > best_score:
            best_score = score
            best_chunk = chunk

    if best_score < min_score:
        return None

    return best_chunk


# ---------------------------------------------------
# GROQ AI FUNCTION
# ---------------------------------------------------
def get_answer_from_groq(context, question):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    prompt = f"""
You are StudySphere AI, a helpful study assistant.

Answer the student's question using ONLY the context below.

If the answer is not present in the context, clearly say:
"Sorry, I could not find this answer in the uploaded document."

Context:
{context}

Question:
{question}

Give a clear, student-friendly answer.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You answer only from the uploaded study document."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=700
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## 📚 Study Companion")

    st.divider()

    st.markdown("### How it works")
    st.markdown("""
    **1. Upload your notes**  
    **2. Ask a question**  
    **3. Get an answer grounded in your document**
    """)

    st.divider()

    st.markdown("### Powered by")
    st.markdown("""
    RAG-style retrieval  
    Groq LLM  
    Streamlit  

    Your document is processed only during this session.
    """)


# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------
st.markdown(
    '<div class="main-brand">📚 StudySphere AI</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
    <h1>Study smarter with your own notes. ✨</h1>
    <p>Upload study material, ask questions, and receive clear answers based only on your document.</p>
</div>
""", unsafe_allow_html=True)

left_column, right_column = st.columns([1.15, 1])

with left_column:
    st.markdown(
        '<div class="section-title">📄 Add your study material</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload a TXT document",
        type=["txt"],
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="section-title">💬 Ask from your notes</div>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "Ask your question",
        placeholder="Example: Explain the difference between supervised and unsupervised learning.",
        height=135,
        label_visibility="collapsed"
    )

    ask_button = st.button("✨ Generate Answer")

with right_column:
    st.markdown(
        '<div class="section-title">Why StudySphere?</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Grounded answers</h3>
            <p>Answers are generated from the content you upload, not random web information.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Quick retrieval</h3>
            <p>Your notes are split into chunks so the app can find relevant study material quickly.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>🔎 Transparent learning</h3>
        <p>You can view the exact retrieved context used to generate every answer.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------
# GENERATE ANSWER
# ---------------------------------------------------
if ask_button:
    if uploaded_file is None:
        st.warning("Please upload a TXT document first.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            document_text = uploaded_file.read().decode("utf-8")

            chunks = chunk_text(document_text)

            best_chunk = get_best_chunk(
                chunks,
                question,
                min_score=1
            )

            if best_chunk is None:
                st.error("Sorry, I could not find relevant information in your document.")

            else:
                with st.spinner("StudySphere AI is reading your notes..."):
                    answer = get_answer_from_groq(best_chunk, question)

                st.markdown("## ✨ Your Answer")

                st.markdown(
                    f'<div class="answer-box">{answer}</div>',
                    unsafe_allow_html=True
                )

                with st.expander("🔎 View retrieved context from your document"):
                    st.write(best_chunk)

        except KeyError:
            st.error(
                "Groq API key is missing. Check your `.streamlit/secrets.toml` file."
            )

        except Exception as error:
            st.error(f"Something went wrong: {error}")