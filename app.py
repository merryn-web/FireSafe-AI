import streamlit as st
from src.rag_engine import ask_firesafe


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="FireSafe-AI",
    page_icon="🔥",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🔥 FireSafe-AI")
st.subheader("Fire Safety & Occupant Egress Plan Review Auditor")

st.write(
    "An AI-powered regulatory decision-support system that retrieves "
    "relevant fire-safety evidence and provides grounded compliance guidance."
)

st.warning(
    "Decision-support only: This system does not replace certified "
    "fire-safety professionals, building authorities, or official code review."
)


# --------------------------------------------------
# User Input
# --------------------------------------------------

st.markdown("### 🏢 Fire Safety Assessment")

building_type = st.selectbox(
    "Select building type:",
    [
        "Residential Building",
        "Office Building",
        "Educational Building",
        "Hospital",
        "Shopping / Commercial Building",
        "Industrial Building",
        "Other"
    ]
)

building_floors = st.number_input(
    "Number of floors:",
    min_value=1,
    max_value=100,
    value=1
)

question = st.text_area(
    "Enter your fire-safety question:",
    placeholder=(
        "Example: What are the components of means of egress?"
    ),
    height=120
)

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

if st.button("🔍 Analyze", type="primary"):

    if not question.strip():
        st.error("Please enter a fire-safety question.")

    else:

        with st.spinner("Retrieving regulatory evidence and generating assessment..."):

            try:
                contextual_question = f"""
Building Type: {building_type}
Number of Floors: {building_floors}

Fire Safety Question:
{question}
"""

                answer, results = ask_firesafe(contextual_question)

                # ------------------------------------------
                # Assessment Summary
                # ------------------------------------------

                st.markdown("### 📋 Assessment Summary")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("🏢 **Building Type**")
                    st.write(building_type)

                with col2:
                    st.markdown("🏢 **Number of Floors**")
                    st.write(building_floors)

                st.markdown("### 🔎 Fire-Safety Question")
                st.info(question)

                # ------------------------------------------
                # AI Assessment
                # ------------------------------------------

                st.markdown("### 📄 AI Assessment")

                answer_lower = answer.lower()

                if "insufficient regulatory evidence" in answer_lower:
                    st.warning("Assessment: Insufficient regulatory evidence for a definitive assessment.")
                else:
                    st.success("Assessment generated from the retrieved regulatory evidence.")

                st.write(answer)

                # ------------------------------------------
                # Retrieved Evidence
                # ------------------------------------------

                st.markdown("### 📚 Retrieved Regulatory Evidence")

                if results:

                    st.success(
                        f"Retrieved {len(results)} relevant regulatory evidence item(s)."
                    )

                    for i, document in enumerate(results, start=1):

                        with st.expander(
                            f"Evidence {i}: "
                            f"{document.metadata.get('topic', 'Regulatory Evidence')}"
                        ):

                            st.write(
                                "**Source:** "
                                + document.metadata.get(
                                    "source",
                                    "Unknown"
                                )
                            )

                            st.write(
                                "**Section:** "
                                + document.metadata.get(
                                    "section",
                                    "Not specified"
                                )
                            )

                            st.write("**Evidence:**")

                            st.write(document.page_content)

                else:

                    st.info(
                        "No regulatory evidence was retrieved."
                    )

            except Exception as e:

                st.error(
                    "An error occurred while processing the assessment."
                )

                st.exception(e)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("🔥 FireSafe-AI")

    st.markdown("### System Components")

    st.write("✅ Regulatory Knowledge Base")
    st.write("✅ ChromaDB Vector Search")
    st.write("✅ Semantic Retrieval")
    st.write("✅ Gemini Generative AI")
    st.write("✅ Grounded Response Generation")
    st.write("✅ Regulatory Guardrails")

    st.markdown("---")

    st.markdown("### Knowledge Source")

    st.write(
        "BIS Guide for Using NBC 2016 – "
        "Fire and Life Safety"
    )

    st.markdown("---")

    st.caption(
        "Prototype for academic and research purposes."
    )