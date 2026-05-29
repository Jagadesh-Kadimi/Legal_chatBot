# ⚖️ Legal ChatBot - AI Powered Legal Assistant

An AI-powered Legal ChatBot built using **Python, Streamlit, LangChain, FAISS, and Generative AI** to provide users with quick and accurate legal information from legal documents.

The system leverages **Retrieval-Augmented Generation (RAG)** to retrieve relevant legal context and generate intelligent responses based on uploaded legal documents. The chatbot is designed to simplify access to legal information and assist users in understanding legal concepts more efficiently.

---

# 📌 Table of Contents

* Project Overview
* Features
* System Architecture
* Technology Stack
* Project Structure
* Installation
* Configuration
* Running the Application
* Workflow
* API & Model Details
* Screenshots
* Future Enhancements
* Challenges Faced
* Learning Outcomes
* Deployment
* Contributing
* License
* Author

---

# 📖 Project Overview

Legal ChatBot is an intelligent legal assistant that enables users to ask legal questions in natural language and receive context-aware answers.

The application uses:

* Retrieval-Augmented Generation (RAG)
* Vector Database (FAISS)
* Document Embeddings
* Large Language Models (LLMs)
* Streamlit Web Interface

The chatbot processes legal documents, converts them into embeddings, stores them in a vector database, and retrieves the most relevant information when answering user queries.

---

# 🚀 Features

### Legal Question Answering

* Ask legal questions in natural language.
* Receive intelligent legal guidance.
* Context-aware responses.

### RAG-Based Architecture

* Retrieves relevant legal document sections.
* Enhances response accuracy.
* Reduces hallucinations.

### Document Processing

* PDF document ingestion.
* Text extraction.
* Chunking and preprocessing.

### Semantic Search

* Vector-based document retrieval.
* Similarity search using FAISS.
* Fast response generation.

### Interactive Chat Interface

* User-friendly Streamlit UI.
* Real-time conversations.
* Chat history management.

### AI-Powered Responses

* Uses Generative AI models.
* Context-driven legal explanations.
* Improved legal information accessibility.

---

# 🏗️ System Architecture

```text
User Query
     │
     ▼
Streamlit Interface
     │
     ▼
LangChain Pipeline
     │
     ├────────► FAISS Vector Store
     │               │
     │               ▼
     │       Relevant Documents
     │
     ▼
Generative AI Model
     │
     ▼
Final Response
     │
     ▼
User
```

---

# 🛠️ Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## AI & NLP

* LangChain
* Google Generative AI
* Large Language Models (LLMs)

## Vector Database

* FAISS

## Document Processing

* PyPDF
* PDF Loaders
* Text Splitters

## Environment Management

* Python Virtual Environment
* dotenv

---

# 📂 Project Structure

```text
Legal_ChatBot/
│
├── app.py
├── ingestion.py
├── requirements.txt
├── .env
├── README.md
│
├── LEGAL-DATA/
│   ├── legal_documents.pdf
│   ├── ipc_documents.pdf
│
├── my_vector_store/
│   ├── index.faiss
│   └── metadata.pkl
│
└── assets/
    ├── screenshots
    └── images
```

---

# ⚙️ Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/Jagadesh-Kadimi/Legal_chatBot.git
cd Legal_chatBot
```

## Step 2: Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuration

Create a `.env` file in the root directory.

```env
GOOGLE_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
```

---

# 📥 Data Ingestion

Before running the chatbot, process legal documents.

```bash
python ingestion.py
```

This step:

1. Reads legal PDFs.
2. Extracts text.
3. Splits text into chunks.
4. Generates embeddings.
5. Stores embeddings in FAISS.

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🔄 Application Workflow

### Step 1

User enters legal question.

### Step 2

Query converted into embeddings.

### Step 3

FAISS retrieves relevant legal content.

### Step 4

Relevant context sent to LLM.

### Step 5

LLM generates answer.

### Step 6

Response displayed in chat interface.

---

# 🧠 RAG Pipeline

The application follows Retrieval-Augmented Generation:

1. Document Loading
2. Text Chunking
3. Embedding Generation
4. Vector Storage
5. Semantic Retrieval
6. LLM Response Generation

Benefits:

* Improved accuracy
* Better context understanding
* Reduced hallucinations
* Faster information retrieval

---

# 📊 Key Advantages

* Legal information available instantly
* Efficient document search
* User-friendly interface
* Scalable architecture
* Domain-specific responses
* AI-assisted legal guidance

---

# 📷 Screenshots

## Home Page

Add screenshot here:

```text
assets/screenshots/home.png
```

## Chat Interface

Add screenshot here:

```text
assets/screenshots/chat.png
```

## Response Example

Add screenshot here:

```text
assets/screenshots/response.png
```

---

# 🚧 Challenges Faced

* Processing large legal documents.
* Managing context length limitations.
* Improving retrieval accuracy.
* Reducing hallucinated responses.
* Optimizing vector search performance.

---

# 📈 Future Enhancements

* Multi-language support.
* Voice-based legal assistant.
* OCR support for scanned documents.
* Legal document summarization.
* Case law recommendations.
* User authentication.
* Admin dashboard.
* Cloud deployment.
* Mobile application.

---

# 🎯 Learning Outcomes

Through this project, I gained practical experience in:

* Retrieval-Augmented Generation (RAG)
* LangChain
* FAISS Vector Databases
* Generative AI Models
* Prompt Engineering
* NLP Applications
* Streamlit Development
* Legal Information Retrieval Systems

---

# ☁️ Deployment

### Streamlit Cloud

```bash
streamlit run app.py
```

Deploy using Streamlit Cloud.

### Render

Deploy backend and configure environment variables.

### Docker (Optional)

```bash
docker build -t legal-chatbot .
docker run -p 8501:8501 legal-chatbot
```

---

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork repository.
2. Create feature branch.
3. Commit changes.
4. Push branch.
5. Create Pull Request.

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

### Jagadesh Kadimi

* GitHub: https://github.com/Jagadesh-Kadimi
* LinkedIn: Add Your LinkedIn Profile

---

⭐ If you found this project useful, please consider giving it a star on GitHub.
