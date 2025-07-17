from pathlib import Path
from langchain.schema import Document

# --- Supported encongs for fallback decoding ---
SUPPORTED_ENCODINGS = ["utf-8", "windows-1252", "ISO-8859-1"]

# --- Supported file types ---
SUPPORTED_EXTENSIONS = [".txt", ".md"]


def load_all_docs_from_data(data_path="data"):
    """
    Load all text and markdown files from the given directory, returning a list of LangChain Document objects
    with metadata including file name, extension, and inferred type.
    """
    documents = []
    data_root = Path(data_path)

    for file_path in data_root.rglob("*"):
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            content = None
            for enc in SUPPORTED_ENCODINGS:
                try:
                    with open(file_path, "r", encoding=enc) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue

            if content:
                documents.append(Document(
                    page_content=content,
                    metadata={
                        "source_file": str(file_path.relative_to(data_path)),
                        "file_extension": file_path.suffix.lower(),
                        "doc_type": "markdown" if file_path.suffix.lower() == ".md" else "text"
                    }
                ))

    return documents