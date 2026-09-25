"""
FireSafe-AI
Build ChromaDB Vector Database

This script:
1. Loads the structured regulatory knowledge base
2. Converts entries into documents
3. Generates embeddings
4. Stores them in ChromaDB
"""

from pathlib import Path
import json

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "regulatory_knowledge.json"
)

CHROMA_DIR = PROJECT_ROOT / "chroma_db"


# --------------------------------------------------
# Load regulatory knowledge
# --------------------------------------------------

def load_knowledge_base():
    """Load the structured regulatory knowledge base."""

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Convert entries to LangChain documents
# --------------------------------------------------

def create_documents(knowledge_base):
    """Convert knowledge entries into LangChain Documents."""

    documents = []

    for item in knowledge_base:

        document = Document(
            page_content=item["content"],
            metadata={
                "id": item["id"],
                "topic": item["topic"],
                "section": item["section"],
                "source": item["source"],
                "source_type": item["source_type"],
            },
        )

        documents.append(document)

    return documents


# --------------------------------------------------
# Build ChromaDB
# --------------------------------------------------

def build_vector_database():

    print("=" * 60)
    print("FireSafe-AI Vector Database Builder")
    print("=" * 60)

    # Load knowledge
    knowledge_base = load_knowledge_base()

    print(f"\nLoaded knowledge entries: {len(knowledge_base)}")

    # Convert to documents
    documents = create_documents(knowledge_base)

    print(f"Created documents: {len(documents)}")

    # Embedding model
    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded.")

    # Create Chroma vector store
    print("\nBuilding ChromaDB...")

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="firesafe_regulations",
        persist_directory=str(CHROMA_DIR),
    )

    print("\nVector database created successfully!")

    print(f"Location: {CHROMA_DIR}")
    print(f"Documents stored: {len(documents)}")

    return vector_store


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":
    build_vector_database()