from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()



def chunk_text(text, chunk_size=500, overlap=50):
    start = 0
    chunks = []
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


CHROMA_PATH = "db/chroma"
EMBED_MODEL = "all-MiniLM-L6-v2"
def create_vector_store(text, collection_name="syllabus_collection"):
    from rag_util import chunk_text  # Or move it to the top if needed
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("No chunks generated from text.")

    # Load embedding model
    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(chunks, show_progress_bar=True)

    # ✅ Use DuckDB instead of SQLite
    chroma_client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=CHROMA_PATH
    ))

    # Delete existing collection if it exists
    if collection_name in [c.name for c in chroma_client.list_collections()]:
        chroma_client.delete_collection(name=collection_name)

    # Create new collection
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Add chunks with their embeddings
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[f"chunk-{i}"]
        )

    return collection



def get_relevant_chunks(query, collection_name="syllabus_collection", top_k=5):
    model = SentenceTransformer(EMBED_MODEL)
    query_embedding = model.encode([query])[0]


    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results['documents'][0]
    return "\n\n".join(documents) if documents else "No relevant chunks found."
