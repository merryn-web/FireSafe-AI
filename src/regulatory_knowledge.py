"""
FireSafe-AI
Initial Regulatory Knowledge Base

Source:
Bureau of Indian Standards (BIS)
Guide for Using National Building Code of India 2016

Scope:
Publicly accessible summary material related to
NBC 2016 Part 4 - Fire and Life Safety.

Important:
This is NOT the complete NBC 2016 code.
Numerical requirements are not invented or assumed.
"""

from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = PROCESSED_DATA_DIR / "regulatory_knowledge.json"


KNOWLEDGE_BASE = [
    {
        "id": "NBC4-001",
        "topic": "Fire and Life Safety",
        "section": "NBC 2016 Part 4",
        "content": (
            "Part 4 of the National Building Code of India 2016 "
            "covers Fire and Life Safety provisions."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-002",
        "topic": "Life Safety",
        "section": "NBC 2016 Part 4",
        "content": (
            "The Life Safety provisions of Part 4 address requirements "
            "intended to support safe movement and evacuation of occupants "
            "during fire and emergency situations."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-003",
        "topic": "Occupant Load",
        "section": "NBC 2016 Part 4",
        "content": (
            "Occupant load is identified as an important consideration "
            "within the life-safety and means-of-egress framework."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-004",
        "topic": "General Exit Requirements",
        "section": "NBC 2016 Part 4",
        "content": (
            "General exit requirements form part of the Life Safety "
            "provisions of NBC 2016 Part 4."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-005",
        "topic": "Exit Access",
        "section": "NBC 2016 Part 4",
        "content": (
            "Exit access is one of the components of the means of "
            "egress described in the NBC 2016 fire and life-safety framework."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-006",
        "topic": "Exit",
        "section": "NBC 2016 Part 4",
        "content": (
            "An exit is identified as one of the components of the "
            "means of egress in the NBC 2016 fire and life-safety framework."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-007",
        "topic": "Exit Discharge",
        "section": "NBC 2016 Part 4",
        "content": (
            "Exit discharge is identified as one of the components of "
            "the means of egress."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-008",
        "topic": "Means of Egress",
        "section": "NBC 2016 Part 4",
        "content": (
            "The means of egress framework consists of exit access, "
            "exit and exit discharge."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },

    {
        "id": "NBC4-009",
        "topic": "Egress Components",
        "section": "NBC 2016 Part 4",
        "content": (
            "Examples of egress components discussed in the NBC framework "
            "include doorways, corridors, passageways, internal staircases, "
            "exit passageways, external staircases and ramps."
        ),
        "source": "BIS Guide for Using NBC 2016",
        "source_type": "official_public_summary",
    },
]


def create_knowledge_base():
    """Create the initial structured regulatory knowledge base."""

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            KNOWLEDGE_BASE,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 60)
    print("FireSafe-AI Regulatory Knowledge Base")
    print("=" * 60)

    print(f"\nCreated: {OUTPUT_FILE}")
    print(f"Number of knowledge entries: {len(KNOWLEDGE_BASE)}")

    print("\nTopics:")

    for item in KNOWLEDGE_BASE:
        print(f"- {item['topic']}")

    print("\nKnowledge base created successfully.")


if __name__ == "__main__":
    create_knowledge_base()