import os
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredImageLoader,
)

def load_documents(data_dir):
    """
    Loads all supported documents from the specified directory.
    
    Supported formats: .pdf, .txt, .md, .png, .jpg, .jpeg
    
    Args:
        data_dir (str): The path to the directory containing the documents.
        
    Returns:
        list: A list of LangChain Document objects.
    """
    documents = []
    supported_files = [f for f in os.listdir(data_dir) if f.endswith(('.pdf', '.txt', '.md', '.png', '.jpg', '.jpeg'))]

    for filename in supported_files:
        filepath = os.path.join(data_dir, filename)
        try:
            if filename.endswith('.pdf'):
                loader = PyMuPDFLoader(filepath)
            elif filename.endswith(('.png', '.jpg', '.jpeg')):
                # This will use pytesseract for OCR
                loader = UnstructuredImageLoader(filepath, mode="single")
            elif filename.endswith('.md'):
                loader = UnstructuredMarkdownLoader(filepath)
            elif filename.endswith('.txt'):
                loader = TextLoader(filepath, encoding='utf-8')
            
            docs = loader.load()
            documents.extend(docs)
            print(f"Successfully loaded {filename}")
        except Exception as e:
            print(f"Failed to load {filename}. Error: {e}")
            
    return documents
