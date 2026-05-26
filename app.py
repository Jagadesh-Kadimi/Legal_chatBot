<<<<<<< HEAD
import streamlit as st
import json
import os
import shutil
from dotenv import load_dotenv

# =========================
# LOAD ENV
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

st.title("⚖️ Indian Legal AI Assistant")
st.markdown(
    "Scenario-based Indian Legal Guidance System"
)

# =========================
# API KEY
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY")
    st.stop()

# =========================
# LOAD IPC DATA ONLY
# =========================

def load_ipc_data():

    documents = []

    if os.path.exists("ipc_sections.json"):

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
                            "section": section,
                            "source": "IPC"
                        }
                    )
                )

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

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    persist_directory = "./legal_db_index"

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
        temperature=0.1
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
    # PROMPT
    # =========================

    custom_template = """
    You are an intelligent Indian Legal Assistant.

    Help users understand:
    - legal issue
    - IPC sections
    - practical next steps
    - evidence required
    - where to complain
    - legal advice

    RESPONSE FORMAT:

    ## 🧾 Situation Analysis

    ## ⚖️ Applicable Law

    ## 🚨 Immediate Steps

    ## 📂 Evidence to Collect

    ## 🏛️ Where to Complain

    ## ⚠️ Important Legal Advice

    ## 👨‍⚖️ Practical Example

    Use ONLY provided legal context.

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

    if st.button("🧹 Clear Conversation"):

        st.session_state.messages = []
        st.rerun()

# =========================
# INIT BOT
# =========================

try:

    qa_bot = setup_qa_chain()

except Exception as e:

    st.error(f"Initialization Error: {e}")
    st.stop()

# =========================
# SESSION
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================
# DISPLAY CHAT
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

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing legal issue..."):

            try:

                enhanced_prompt = f"""
                Analyze this Indian legal issue:

                {prompt}

                Provide:
                - legal analysis
                - IPC sections
                - practical next steps
                - complaint methods
                - legal guidance
                """

                response = qa_bot.invoke({
                    "question": enhanced_prompt
                })

                answer = response["answer"]

                st.markdown(answer)

            except Exception as e:

                answer = f"Error: {str(e)}"

                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
=======
import streamlit as st
import json
import os
import shutil

# =========================
# LANGCHAIN IMPORTS
# =========================

from transformers import pipeline

from langchain_community.llms import HuggingFacePipeline
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

st.title("⚖️ Indian Legal AI Assistant")
st.markdown(
    "Scenario-Based Indian Legal Assistant using IPC Sections and Court Judgements"
)

# =========================
# LOAD & PROCESS DATA
# =========================

def load_and_process_data():

    documents = []

    # --------------------------------
    # IPC DATA
    # --------------------------------

    if os.path.exists("ipc_sections.json"):

        with open("ipc_sections.json", "r", encoding="utf-8") as f:

            ipc_data = json.load(f)

            if isinstance(ipc_data, dict):
                ipc_data = [ipc_data]

            for item in ipc_data:

                section = item.get("Section", "Unknown")
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

    # --------------------------------
    # COURT JUDGEMENTS
    # --------------------------------

    if os.path.exists("judgements.json"):

        with open("judgements.json", "r", encoding="utf-8") as f:

            judgments = json.load(f)

            # LIMIT FOR FAST TESTING
            for j in judgments[:3000]:

                title = j.get("title", "")
                act = j.get("act", "")
                judge = j.get("judge", "")

                headnote = ""

                if isinstance(j.get("headnote_sent"), list):
                    headnote = " ".join(j["headnote_sent"])

                text = f"""
                Case Title:
                {title}

                Act:
                {act}

                Judge:
                {judge}

                Headnote:
                {headnote}
                """

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": "Judgement",
                            "case_title": title
                        }
                    )
                )

    # --------------------------------
    # TEXT SPLITTING
    # --------------------------------

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

    # --------------------------------
    # EMBEDDINGS
    # --------------------------------

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
        # model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    persist_directory = "./legal_db_index"

    # --------------------------------
    # VECTOR DATABASE
    # --------------------------------

    if not os.path.exists(persist_directory):

        with st.spinner("Creating legal vector database..."):

            docs = load_and_process_data()

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

    # --------------------------------
    # FREE LOCAL HUGGINGFACE MODEL
    # --------------------------------

    pipe = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=200
)

    llm = HuggingFacePipeline(
        pipeline=pipe
    )

    # --------------------------------
    # MEMORY
    # --------------------------------

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # --------------------------------
    # PROMPT TEMPLATE
    # --------------------------------

    custom_template = """
    You are an intelligent Indian Legal Assistant.

    Your goal is NOT to simply explain laws.

    Your goal is to help normal people understand:
    - what happened legally
    - what crime may apply
    - what actions they should take
    - practical next steps
    - legal remedies available in India

    Use ONLY the provided legal context.

    ----------------------------------------

    RESPONSE FORMAT:

    ## 🧾 Situation Analysis
    Briefly explain what legal issue is happening.

    ## ⚖️ Applicable Law
    Mention relevant IPC sections and laws clearly.

    ## 🚨 Immediate Steps
    Explain what the person should do immediately.

    ## 📂 Evidence to Collect
    Mention useful proofs or evidence.

    ## 🏛️ Where to Complain
    Mention:
    - Police
    - Cybercrime portal
    - Court
    - Consumer forum
    - Women's helpline
    etc if relevant.

    ## ⚠️ Important Legal Advice
    Mention cautions, rights, or important legal notes.

    ## 👨‍⚖️ Practical Example
    Give one real-life style example.

    ----------------------------------------

    RULES:
    - Speak like a practical legal advisor
    - Avoid overly technical legal jargon
    - Use simple understandable English
    - Never hallucinate laws
    - Never invent punishments
    - If context insufficient say:
    "I could not find enough legal records."

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

    # --------------------------------
    # QA CHAIN
    # --------------------------------

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,

        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 8}
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

    if st.button("🗑️ Rebuild Legal Database"):

        if os.path.exists("./legal_db_index"):

            shutil.rmtree("./legal_db_index")

        st.success("Legal database deleted.")
        st.info("Restart app now.")

    st.divider()

    if st.button("🧹 Clear Conversation"):

        st.session_state.messages = []
        st.rerun()

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

if prompt:

    # Store user message

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message

    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant response

    with st.chat_message("assistant"):

        with st.spinner("Analyzing legal records..."):

            try:

                enhanced_prompt = f"""
                                Analyze this Indian legal situation carefully:

                                {prompt}

                                Provide:
                                - legal analysis
                                - applicable IPC sections
                                - immediate practical steps
                                - evidence required
                                - complaint options
                                - legal advice
                                - citizen guidance
                                """
                response = qa_bot.invoke({
                    "question": enhanced_prompt
                })

                answer = response["answer"]

                st.markdown(answer)

                # --------------------------------
                # SHOW SOURCES
                # --------------------------------

                with st.expander("📚 Legal Sources Used"):

                    for i, doc in enumerate(
                        response["source_documents"],
                        start=1
                    ):

                        st.markdown(f"## Source {i}")

                        st.code(doc.page_content[:1200])

                        st.json(doc.metadata)

                        st.divider()

            except Exception as e:

                answer = f"❌ Error: {str(e)}"

                st.error(answer)

    # Save assistant response

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
>>>>>>> 950852e0274a6cecf77207cd715c62c9a039a50b
