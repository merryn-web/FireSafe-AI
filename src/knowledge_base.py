from pathlib import Path
from pypdf import PdfReader


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def find_pdf():
    """Find the first PDF inside data/raw."""
    pdf_files = list(RAW_DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF found. Please place the regulatory PDF inside data/raw/"
        )

    return pdf_files[0]


def extract_pdf_text(pdf_path):
    """Extract text from every page of the PDF."""
    reader = PdfReader(str(pdf_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text
        })

    return pages


def main():
    print("=" * 60)
    print("FireSafe-AI - Regulatory Knowledge Base")
    print("=" * 60)

    pdf_path = find_pdf()

    print(f"\nPDF found: {pdf_path.name}")

    pages = extract_pdf_text(pdf_path)

    print(f"Number of pages: {len(pages)}")

    total_characters = sum(len(page["text"]) for page in pages)

    print(f"Extracted characters: {total_characters:,}")

    print("\n--- First page preview ---\n")

    if pages:
        preview = pages[0]["text"][:3000]
        print(preview)

    print("\n" + "=" * 60)
    print("PDF extraction completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()