# 🧠 NeuroNexus – RAG Model (Ollama + Gemini + ChromaDB)

NeuroNexus is a **Retrieval-Augmented Generation (RAG)** based chatbot that can **read PDF documents and answer user queries contextually**.  
The system combines **local LLMs via Ollama** and **cloud-based Gemini API** with **ChromaDB vector storage** to deliver accurate, document-grounded responses.

This project is designed to run **locally on Windows** and focuses on **simplicity, reliability, and clean UI**, making it ideal for academic demos and project evaluations.

---

## 🚀 Features

- 📄 Upload and process PDF documents
- 🔍 Context-aware question answering
- 🧠 Dual LLM support:
  - **Ollama (Local LLM fallback)**
  - **Google Gemini API (Primary cloud LLM)**
- 🧩 Automatic fallback if one model fails
- 📦 Vector storage using **ChromaDB**
- 🧠 Token-based text chunking and embeddings
- 💬 Chatbot-style interactive UI
- ⚡ Fast semantic search and response generation
- 🖥️ Fully local execution (no production setup required)

---

## 🏗️ Architecture (High-Level)

User Query
↓
PDF Loader
↓
Text Chunking
↓
Embedding Generation
↓
ChromaDB Vector Store
↓
Relevant Context Retrieval
↓
LLM (Gemini / Ollama)
↓
Final Answer

---

## 🛠️ Tech Stack

### 🔹 Backend & AI
- Python 3.10+
- LangChain
- Google Gemini API
- Ollama (Local LLMs)
- ChromaDB (Vector Database)

### 🔹 Embeddings
- Token-based text embeddings
- Semantic similarity search

### 🔹 Frontend / UI
- Streamlit (Chat-style interface)

---

## 📂 Project Structure

NeuroNexus-RAG-Model/
│
├── main.py # Main application logic
├── prompt.py # RAG prompt template
├── env.py # API key loader
├── requirements.txt # Dependencies
├── data/ # Uploaded PDF files
├── chroma_db/ # Vector database storage
├── README.md # Project documentation
└── .env # Environment variables (ignored)

---

## ⚙️ Installation & Setup (Windows)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/xenonrocks71/NeuroNexus-RAG-Model.git
cd NeuroNexus-RAG-Model
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

🔑 Environment Configuration

Create a .env file in the root directory:

GOOGLE_API_KEY=your_gemini_api_key_here


⚠️ Do NOT upload .env to GitHub

▶️ Running the Application
streamlit run main.py


Then open your browser at:

http://localhost:8501

🧪 How It Works

User uploads a PDF

Text is extracted and split into chunks

Embeddings are generated for each chunk

Chunks are stored in ChromaDB

User query is embedded and matched

Relevant context is passed to:

Gemini API (primary)

Ollama (fallback)

Final grounded answer is generated

🤖 Supported Models
Ollama (Local)

LLaMA

Mistral

Gemma

Any Ollama-supported model

Gemini (Cloud)

Gemini Pro / Flash

🎯 Use Cases

Academic document analysis

Project reports Q&A

Research paper understanding

Internal knowledge assistants

AI demos and viva presentations

📌 Future Enhancements

Multi-PDF support

Conversation memory

Source citation in responses

Model selection toggle in UI

Docker support

👨‍💻 Author

Mayur Patil
B.Tech Computer Engineering
Dr. Babasaheb Ambedkar Technological University, Lonere

⭐ Acknowledgements

LangChain

Google Gemini

Ollama

ChromaDB

Streamlit

📜 License

This project is for educational and academic purposes only.
