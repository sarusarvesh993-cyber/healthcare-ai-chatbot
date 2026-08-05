import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


def create_vector_store():
    print("=" * 60)
    print("Healthcare Chatbot - Vector Store Creator")
    print("=" * 60)

    kb_path = os.path.join(os.path.dirname(__file__), "medical_knowledge_base.json")
    print(f"\n[1/5] Loading knowledge base from: {kb_path}")

    with open(kb_path, "r") as f:
        knowledge_base = json.load(f)

    print(f"      Loaded {len(knowledge_base)} documents")

    print("\n[2/5] Converting to LangChain Documents...")
    documents = []
    for entry in knowledge_base:
        doc = Document(
            page_content=entry["content"],
            metadata={
                "id": entry["id"],
                "topic": entry["topic"],
                "source": entry["source"],
                "category": entry["category"],
            },
        )
        documents.append(doc)

    print(f"      Created {len(documents)} Document objects")

    print("\n[3/5] Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    print(f"      Created {len(chunks)} text chunks")

    print("\n[4/5] Initializing embeddings (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    print("      Embeddings model loaded")

    print("\n[5/5] Creating FAISS vector store...")
    store_path = os.path.join(os.path.dirname(__file__), "faiss_medical_store")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(store_path)

    print(f"\nVector store saved to: {store_path}")
    print(f"Total vectors: {vector_store.index.ntotal}")
    print("\n" + "=" * 60)
    print("Vector store creation complete!")
    print("=" * 60)


if __name__ == "__main__":
    create_vector_store()
