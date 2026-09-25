"""
FireSafe-AI
RAG Engine

Pipeline:
User Question
      ↓
ChromaDB Retrieval
      ↓
Regulatory Evidence
      ↓
Gemini
      ↓
Grounded Response

Important guardrail:
The model must not invent regulatory requirements.
If the retrieved evidence is insufficient, it must say so.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
import spacy

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_ROOT / "chroma_db"


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

client = genai.Client(api_key=api_key)



# --------------------------------------------------
# Load ChromaDB
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
# Extract entities from building information
# --------------------------------------------------

def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities


# --------------------------------------------------
# Retrieve regulatory evidence
# --------------------------------------------------

def retrieve_evidence(vector_store, question, k=3):

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results


# --------------------------------------------------
# Build evidence text
# --------------------------------------------------

def format_evidence(results):

    evidence_parts = []

    for i, document in enumerate(results, start=1):

        topic = document.metadata.get("topic", "Unknown")
        section = document.metadata.get("section", "Unknown")
        source = document.metadata.get("source", "Unknown")

        evidence = f"""
Evidence {i}
Topic: {topic}
Section: {section}
Source: {source}

Content:
{document.page_content}
"""

        evidence_parts.append(evidence)

    return "\n".join(evidence_parts)


# --------------------------------------------------
# Generate grounded answer
# --------------------------------------------------

def generate_answer(question, evidence):

    system_instruction = """
You are FireSafe-AI, a regulatory fire-safety review assistant.

Your task is to answer questions using ONLY the regulatory
evidence provided to you.

IMPORTANT RULES:

1. Do not invent NBC requirements.
2. Do not invent numerical thresholds.
3. Do not use general knowledge to fill missing regulatory information.
4. Do not claim that a building is compliant unless the provided
   evidence actually supports that conclusion.
5. If the evidence is insufficient, clearly state:

   "Insufficient regulatory evidence for a definitive assessment."

6. Identify the relevant topic and source from the evidence.
7. Clearly distinguish between:
   - information explicitly supported by the evidence
   - information that cannot be determined from the evidence
8. This system is a decision-support tool and does not replace
   review by qualified fire-safety professionals or authorities.
"""

    prompt = f"""
USER QUESTION:
{question}

RETRIEVED REGULATORY EVIDENCE:
{evidence}

Using only the evidence above, provide a concise response.

Structure your response as:

Assessment:
[Your evidence-based assessment]

Regulatory Evidence:
[Relevant evidence used]

Source:
[Source name]

Limitations:
[What cannot be determined from the available evidence]
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "system_instruction": system_instruction
        }
    )

    return response.text


# --------------------------------------------------
# Complete RAG pipeline
# --------------------------------------------------

def ask_firesafe(question):

    vector_store = load_vector_store()

    results = retrieve_evidence(
        vector_store,
        question,
        k=3
    )

    evidence = format_evidence(results)

    answer = generate_answer(
        question,
        evidence
    )

    return answer, results


# --------------------------------------------------
# Interactive test
# --------------------------------------------------
if __name__ == "__main__":
    question = "What are the components of means of egress?"

    print("\nQuestion:", question)

    answer, results = ask_firesafe(question)

    print("\n" + answer)

    print("\n" + "=" * 60)
    print("Retrieved Evidence")
    print("=" * 60)

    for i, document in enumerate(results, start=1):

        print(f"\n--- Evidence {i} ---")
        print(f"Topic: {document.metadata.get('topic')}")
        print(f"Source: {document.metadata.get('source')}")