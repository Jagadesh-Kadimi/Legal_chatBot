import json
import os

from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("Loading IPC data...")

documents = []

with open(
    "ipc_sections.json",
    "r",
    encoding="utf-8"
) as f:

    ipc = json.load(f)

    if isinstance(ipc, dict):
        ipc = [ipc]

    for item in ipc:

        text = f"""
        Section: {item.get('Section')}

        Title:
        {item.get('section_title')}

        Description:
        {item.get('section_desc')}
        """

        documents.append(
            Document(page_content=text)
        )

print(f"Loaded {len(documents)} documents")

print("Loading embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
)

persist_directory = "legal_db_index"

# Remove old DB if exists

if os.path.exists(persist_directory):

    import shutil
    shutil.rmtree(persist_directory)

print("Creating vector database...")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=persist_directory
)

print("✅ legal_db_index created successfully")