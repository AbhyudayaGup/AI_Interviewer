import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- Configuration ---
# Define the embedding model to use. "all-MiniLM-L6-v2" is a great starting point.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# Define the directory to persist the vector store
PERSIST_DIRECTORY = "db"

def get_embedding_function():
    """
    Initializes and returns the embedding function.
    """
    # Use CUDA if available, otherwise CPU
    model_kwargs = {'device': 'cuda' if os.environ.get('CUDA_is_available') else 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings

def create_vector_store(chunks):
    """
    Creates a ChromaDB vector store from document chunks.
    
    Args:
        chunks (list): A list of document chunks.
        
    Returns:
        Chroma: The created ChromaDB vector store instance.
    """
    embedding_function = get_embedding_function()
    
    # Create the vector store, persisting it to disk
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    
    return vector_store

def load_vector_store():
    """
    Loads an existing ChromaDB vector store from disk.
    
    Returns:
        Chroma: The loaded ChromaDB vector store instance, or None if it doesn't exist.
    """
    if not os.path.exists(PERSIST_DIRECTORY):
        return None
        
    embedding_function = get_embedding_function()
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_function
    )
    return vector_store
