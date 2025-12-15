import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI

import tempfile
import os
from prompt import RAG_TEMPLATE
from env import get_api


# -------------------------------------------
# Streamlit UI Configuration
# -------------------------------------------
st.set_page_config(
    page_title="NEURONEXUS RAG",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

api_key = get_api()

# ---------------- NEW UI ------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Main background */
.main {
    background: radial-gradient(circle at top, #1f1c2c, #0f0c29);
    color: white !important;
}

/* Glass container */
.block-container {
    background: rgba(255, 255, 255, 0.07);
    padding: 2rem 3rem;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, .1);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(20, 20, 35, 0.75);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
    color: #00D1FF !important;
}

/* Sidebar elements */
.sidebar-item {
    padding: .6rem;
    border-radius: 12px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#0061ff,#60efff);
    border-radius: 10px;
    color: white;
    border: none;
    padding: .7rem;
    font-weight: 600;
    margin-top: 10px;
    transition: .2s;
}
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(0,209,255,0.5);
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    margin: 8px 0;
    padding: 1rem;
    border-radius: 14px;
}

[data-testid="stChatMessageUser"] {
    background: linear-gradient(135deg,#00378f,#0074ff);
    color: white;
}

[data-testid="stChatMessageAssistant"] {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Scrollbar */
::-webkit-scrollbar {width: 8px;}
::-webkit-scrollbar-thumb {background: #00d1ff; border-radius: 10px;}

</style>
""", unsafe_allow_html=True)
# --------------------------------------------------


# Session States (unchanged)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "mode" not in st.session_state:
    st.session_state.mode = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None


# ---------------- Backend Code (UNCHANGED) ----------------
def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        pdf_path = tmp.name

    with st.status("📄 Processing PDF...", expanded=True):
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(chunks, embedding=embeddings)

    os.unlink(pdf_path)
    return vectorstore


def get_response(question, vectorstore):
    with st.status("🤖 Generating…", expanded=False):
        retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 8})
        docs = retriever.invoke(question)
        context = "\n\n".join([d.page_content for d in docs])

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
        prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
        final_prompt = prompt.format(context=context, question=question)

        response_box = st.empty()
        answer = ""

        for chunk in llm.stream(final_prompt):
            if chunk.content:
                answer += chunk.content
                response_box.markdown(answer)

    return answer


# ---------------- Sidebar UI ----------------
with st.sidebar:
    st.markdown("## ⚡ NEURONEXUS RAG")
    st.write("---")

    uploaded_file = st.file_uploader(
        "📤 Upload a PDF",
        type=["pdf"],
        help="Upload a document to chat with it"
    )

    if uploaded_file:
        if st.button("🚀 Process Document"):
            st.session_state.vectorstore = process_pdf(uploaded_file)
            st.session_state.mode = "pdf"
            st.session_state.document_name = uploaded_file.name
            st.session_state.messages = []
            st.success("Document processed!")
            st.rerun()

    if st.session_state.vectorstore:
        st.write("---")
        if st.button("🗑 Reset Session"):
            st.session_state.messages = []
            st.session_state.vectorstore = None
            st.rerun()


# ---------------- Main Chat UI ----------------
st.title("💬 Chat with NEURONEXUS")

if not st.session_state.vectorstore:
    st.markdown("""
    <div style='text-align:center; margin-top:2rem;'>
        <h2>📄 Upload a document to begin.</h2>
        <p style="opacity:.7;">Supports RAG with advanced AI comprehension</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about your document...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = get_response(user_input, st.session_state.vectorstore)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()