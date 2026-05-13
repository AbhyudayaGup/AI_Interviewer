from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):
    """
    Splits a list of LangChain Documents into smaller chunks.
    
    Args:
        documents (list): A list of LangChain Document objects.
        
    Returns:
        list: A list of smaller Document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks
