"""
This is used to load a document and split it into chunks.
Call the function get_final_document to get the final document object.
"""
from langchain_core.documents import Document
from typing import List
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from modules.customLogger import setup_logger

logger = setup_logger()

# Types of files to scan (Markdown / recursive)
GLOB = "**/*.md"

# Markdown Text Splitter headers (not working)
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

# Recursive Character Text Splitter Chunking
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 512
SEPARATORS = ["\n\n", "\n", "(?<=\. )", " ", ""]

# Define Recursive Character Text Splitter
r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, separators=SEPARATORS
)


# Function to split markdown document into chunks
def markdown_split_document(documents: any) -> any:
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    return markdown_splitter.split_text(documents)


# Load Directory
def load_directory(filepath: str) -> List[Document]:
    """
    Loads all documents from the specified directory using the DirectoryLoader with a predefined glob pattern.
    
    Args:
        filepath (str): The path to the directory containing markdown files.
        
    Returns:
        List[Document]: A list of Document objects loaded from the specified directory.
        
    Raises:
        FileNotFoundError: If there is an error loading documents from the specified filepath.
    """
    try:
        logger.info("Loading document from %s", filepath)
        loader = DirectoryLoader(filepath, glob=GLOB, use_multithreading=False, show_progress=True)     # Multithreading not working
        documents = loader.load()
        logger.info("Document loaded from %s", filepath)
        # Return the LangChain documents object
        return documents
    except Exception as e:
        logger.error("Error loading document from %s: %s", filepath, e)
        raise FileNotFoundError(f"Error loading document from {filepath}: {e}")

# Get Final Document Object
def get_final_document(filepath: str, split: bool) -> list | str:
    documents = load_directory(filepath)

    if split:
        logger.info("Documents will be splitted into chunks")
        return r_splitter.split_documents(documents)
    else:
        logger.info("Documents will not be splitted into chunks")
        return documents


# Example usage
if __name__ == "__main__":

    # For module testing only

    # Folder Path
    FOLDERPATH = "docs"

    # Test Get Final Document Object
    print("[i] =====>>> Get Final Document Object")
    print(get_final_document(FOLDERPATH, True))
