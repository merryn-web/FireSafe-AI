"""
FireSafe-AI
RAG Retrieval Test

Tests whether ChromaDB retrieves relevant
regulatory information for user questions.
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "chroma_db"


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        collection_name="firesafe_regulations",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    return vector_store


# --------------------------------------------------
# Test retrieval
# --------------------------------------------------

def test_query(vector_store, query):

    print("\n" + "=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)

    results = vector_store.similarity_search(
        query,
        k=3
    )

    print(f"\nRetrieved documents: {len(results)}")

    for i, document in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")

        print(f"Topic: {document.metadata.get('topic')}")
        print(f"Section: {document.metadata.get('section')}")
        print(f"Source: {document.metadata.get('source')}")

        print(f"\nContent:")
        print(document.page_content)


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("FireSafe-AI RAG Retrieval Test")
    print("=" * 60)

    vector_store = load_vector_store()

    test_queries = [
        "What are the components of means of egress?",
        "What does NBC 2016 Part 4 cover?",
        "What is exit access?",
        "What are examples of egress components?"
    ]

    for query in test_queries:
        test_query(vector_store, query)

    print("\n" + "=" * 60)
    print("Retrieval testing completed.")
    print("=" * 60)