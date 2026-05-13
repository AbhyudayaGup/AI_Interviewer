import os
import argparse
from dotenv import load_dotenv
from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.vector_store import create_vector_store

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function to run the RAG ingestion pipeline.
    This script loads documents from the data directory, splits them into chunks,
    generates embeddings, and stores them in a vector database.
    """
    print("Starting RAG ingestion pipeline...")

    # 1. Load documents from the data directory
    print("Step 1: Loading documents from '/data' directory...")
    documents = load_documents('data')
    if not documents:
        print("No documents found. Exiting.")
        return
    print(f"Loaded {len(documents)} documents.")

    # 2. Split documents into chunks
    print("Step 2: Splitting documents into manageable chunks...")
    chunks = split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    # 3. Create and populate the vector store
    print("Step 3: Creating vector store and generating embeddings...")
    try:
        vector_store = create_vector_store(chunks)
        print("Vector store created successfully.")
        # A simple check to confirm persistence
        print(f"Vector store contains {vector_store._collection.count()} embeddings.")
        print("RAG ingestion pipeline completed successfully!")
    except Exception as e:
        print(f"An error occurred during vector store creation: {e}")
        print("Please check your HuggingFace API token and model configuration.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the RAG ingestion pipeline.")
    # No arguments needed for now, but can be extended
    args = parser.parse_args()
    main()
