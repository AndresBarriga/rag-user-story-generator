from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.schema import Document

def split_documents(documents):
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "heading1"), ("##", "heading2")])
    chunker = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = []

    for doc in documents:
        header_sections = header_splitter.split_text(doc.page_content)
        for i, section in enumerate(header_sections):
            if hasattr(section, 'page_content'):
                section_text = section.page_content
            else:
                section_text = str(section)

            section_chunks = chunker.split_text(section_text)

            for j, chunk in enumerate(section_chunks):
                chunks.append(Document(
                    page_content=chunk,
                    metadata={**doc.metadata, "header_chunk_index": i, "chunk_index": j}
                ))

    return chunks

if __name__ == "__main__":
    from data_loader import load_all_docs_from_data 

    docs = load_all_docs_from_data("data")
    chunks = split_documents(docs)
    print(f"Total chunks created: {len(chunks)}")
    print(chunks[0].page_content[:300])
    print(chunks[0].metadata)
