import sys
import platform

# Use pysqlite3 only on Linux/Render
if platform.system() != "Windows":
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import streamlit as st
import json
import os

# =========================
# UPDATED IMPORTS
# =========================

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
# =========================
# SETTINGS
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Legal AI Assistant",
    layout="wide"
)

st.title("⚖️ Indian Legal Assistant")

st.markdown("""
Providing legal clarity using IPC sections.
""")

# =========================
# LOAD DATA
# =========================

def load_and_process_data():

    documents = []

    # ONLY IPC DATA
    # Removed huge judgments dataset

    if os.path.exists('ipc_sections.json'):

        with open(
            'ipc_sections.json',
            'r',
            encoding='utf-8'
        ) as f:

            ipc = json.load(f)

            if isinstance(ipc, dict):
                ipc = [ipc]

            for item in ipc:

                text = f"""
                Section {item.get('Section')}

                Title:
                {item.get('section_title')}

                Description:
                {item.get('section_desc')}
                """

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": "ipc_sections.json"
                        }
                    )
                )

    return documents

# =========================
# BUILD VECTOR DB
# RUN ONLY ONCE LOCALLY
# =========================

@st.cache_resource
def setup_qa_chain():

    st.write("⏳ Loading embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
    )

    st.write("✅ Embeddings loaded")

    persist_directory = "./legal_db_index"

    # =========================
    # LOAD EXISTING DB ONLY
    # =========================

    if not os.path.exists(persist_directory):

        st.error("""
        legal_db_index folder missing.

        Run create_db.py locally first.
        """)

        st.stop()

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    st.write("✅ Vector database loaded")

    # =========================
    # LLM
    # =========================

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.1
    )

    st.write("✅ Groq connected")

    # =========================
    # MEMORY
    # =========================

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key='answer'
    )

    # =========================
    # PROMPT
    # =========================

    template = """
    You are an Indian Legal Assistant.

    Explain:
    - applicable IPC sections
    - legal steps
    - complaint methods
    - evidence required

    Context:
    {context}

    Chat History:
    {chat_history}

    Question:
    {question}

    Helpful Answer:
    """

    QA_PROMPT = PromptTemplate(
        template=template,
        input_variables=[
            "context",
            "chat_history",
            "question"
        ]
    )

    return ConversationalRetrievalChain.from_llm(

        llm=llm,

        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 3}
        ),

        memory=memory,

        combine_docs_chain_kwargs={
            "prompt": QA_PROMPT
        },

        return_source_documents=True
    )

# =========================
# SESSION
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================
# INIT BOT
# =========================

try:

    qa_bot = setup_qa_chain()

except Exception as e:

    st.error(f"Error initializing: {e}")

    st.stop()

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header("⚙️ Settings")

    if st.button(
        "🧹 Clear Conversation",
        key="clear_chat_btn"
    ):

        st.session_state.messages = []

        st.rerun()

# =========================
# DISPLAY CHAT
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================
# CHAT INPUT
# =========================

if prompt := st.chat_input(
    "Ask a legal question..."
):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing legal records..."
        ):

            try:

                response = qa_bot.invoke({
                    "question": prompt
                })

                answer = response['answer']

                st.markdown(answer)

                with st.expander(
                    "📚 Show Legal Sources Used"
                ):

                    for doc in response[
                        'source_documents'
                    ]:

                        st.info(
                            f"Source: "
                            f"{doc.metadata['source']}\n\n"
                            f"{doc.page_content[:400]}..."
                        )

            except Exception as e:

                answer = f"❌ Error: {str(e)}"

                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })