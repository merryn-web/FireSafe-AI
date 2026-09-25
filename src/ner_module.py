import spacy

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    """
    Extract named entities from fire-safety related text.
    """

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities
if __name__ == "__main__":

    test_text = """
    This is an educational building with 180 occupants,
    3 floors, a corridor width of 1.2 m,
    an exit door width of 1.0 m and a travel distance of 30 m.
    """

    entities = extract_entities(test_text)

    print("=" * 60)
    print("FireSafe-AI NER TEST")
    print("=" * 60)

    for entity in entities:
        print(
            f"Entity: {entity['text']} | "
            f"Type: {entity['label']}"
        )