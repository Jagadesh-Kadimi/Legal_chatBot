import streamlit as st
import json
import os
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# LANGCHAIN IMPORTS
# =========================

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Indian Legal AI Assistant",
    layout="wide"
)

# =========================
# APP TITLE
# =========================

st.title("⚖️ Indian Legal AI Assistant")

st.markdown("""
Scenario-Based Indian Legal Guidance System

Ask questions about:
- Cybercrime
- Fraud
- Harassment
- Property disputes
- Consumer complaints
- IPC sections
- Police complaints
- Legal guidance
""")

# =========================
# API KEY
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:

    st.error("❌ Missing GROQ_API_KEY")

    st.info("""
    Add GROQ_API_KEY:

    LOCAL:
    Create .env file

    RENDER:
    Dashboard → Environment
    """)

    st.stop()

# =========================
# LOAD IPC DATA
# =========================

def load_ipc_data():

    documents = []

    if not os.path.exists("ipc_sections.json"):

        st.error("ipc_sections.json file missing")
        return documents

    try:

        with open(
            "ipc_sections.json",
            "r",
            encoding="utf-8"
        ) as f:

            ipc_data = json.load(f)

        if isinstance(ipc_data, dict):
            ipc_data = [ipc_data]

        for item in ipc_data:

            section = item.get("Section", "")
            title = item.get("section_title", "")
            desc = item.get("section_desc", "")

            text = f"""
            IPC Section: {section}

            Title:
            {title}

            Description:
            {desc}
            """

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": "IPC",
                        "section": section
                    }
                )
            )

    except Exception as e:

        st.error(f"Error loading IPC data: {e}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    split_docs = splitter.split_documents(documents)

    return split_docs

# =========================
# SETUP QA CHAIN
# =========================

@st.cache_resource
def setup_qa_chain():

    # =========================
    # EMBEDDINGS
    # =========================

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    persist_directory = "./legal_db_index"

    # =========================
    # VECTOR DATABASE
    # =========================

    if not os.path.exists(persist_directory):

        with st.spinner("Creating legal database..."):

            docs = load_ipc_data()

            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory=persist_directory
            )

    else:

        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

    # =========================
    # GROQ MODEL
    # =========================

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.2
    )

    # =========================
    # MEMORY
    # =========================

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # =========================
    # PROMPT TEMPLATE
    # =========================

    custom_template = """
    You are an intelligent Indian Legal Assistant.

    Your goal:
    - Explain legal issues clearly
    - Mention IPC sections
    - Give practical legal guidance
    - Help common people understand legal actions

    RESPONSE FORMAT:

    ## 🧾 Situation Analysis

    ## ⚖️ Applicable Law

    ## 🚨 Immediate Steps

    ## 📂 Evidence to Collect

    ## 🏛️ Where to Complain

    ## ⚠️ Important Legal Advice

    ## 👨‍⚖️ Practical Example

    IMPORTANT:
    - Use simple English
    - Avoid unnecessary legal jargon
    - Never invent laws
    - Never hallucinate punishments
    - Use ONLY provided context

    Context:
    {context}

    Chat History:
    {chat_history}

    Question:
    {question}

    Helpful Legal Guidance:
    """

    CUSTOM_PROMPT = PromptTemplate(
        template=custom_template,
        input_variables=[
            "context",
            "chat_history",
            "question"
        ]
    )

    # =========================
    # QA CHAIN
    # =========================

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,

        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        ),

        memory=memory,

        combine_docs_chain_kwargs={
            "prompt": CUSTOM_PROMPT
        },

        return_source_documents=True
    )

    return qa_chain

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

    st.divider()

    st.markdown("""
    ### ℹ️ Features

    ✅ IPC Section Guidance  
    ✅ Scenario-Based Advice  
    ✅ Legal Steps  
    ✅ Complaint Guidance  
    ✅ Evidence Suggestions  
    """)

# =========================
# INITIALIZE BOT
# =========================

try:

    qa_bot = setup_qa_chain()

except Exception as e:

    st.error(f"Initialization Error: {e}")

    st.stop()

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================
# USER INPUT
# =========================

prompt = st.chat_input(
    "Ask your legal question..."
)

# =========================
# PROCESS USER INPUT
# =========================

if prompt:

    # Store User Message

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display User Message

    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant Response

    with st.chat_message("assistant"):

        with st.spinner("Analyzing legal issue..."):

            try:

                enhanced_prompt = f"""
                Analyze this Indian legal issue carefully:

                {prompt}

                Provide:
                - legal analysis
                - IPC sections
                - immediate steps
                - complaint methods
                - evidence required
                - practical legal advice
                """

                response = qa_bot.invoke({
                    "question": enhanced_prompt
                })

                answer = response["answer"]

                st.markdown(answer)

                # =========================
                # SOURCE DOCUMENTS
                # =========================

                with st.expander("📚 Legal Sources Used"):

                    for i, doc in enumerate(
                        response["source_documents"],
                        start=1
                    ):

                        st.markdown(f"### Source {i}")

                        st.code(
                            doc.page_content[:1000]
                        )

                        st.json(doc.metadata)

                        st.divider()

            except Exception as e:

                answer = f"❌ Error: {str(e)}"

                st.error(answer)

    # Save Assistant Message

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })