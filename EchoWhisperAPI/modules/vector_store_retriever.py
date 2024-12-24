"""
This is used to create a vector store.
Call the function query_vector_store_as_retriever or other query functions to get the final document context.

The document is loaded from the moduel doc_loader_splitter_md.py
"""

from modules.doc_loader_splitter_md import get_final_document
# from doc_loader_splitter_md import get_final_document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_core.documents import Document
import shutil
from modules.customLogger import setup_logger

logger = setup_logger()

# Document Folder Path
FOLDERPATH = "docs"

# Embedding Model
EMBEDDING_MODEL = "nomic-embed-text:latest"

# Persist Directory
PERSIST_DIRECTORY = "VectorStore/chroma_db"

# Number of results (k)
NUM_RESULTS = 1

# Diversity of Retriever
MMR_DIVERSITY = 0.5
# lambda_mult: Diversity of results returned by MMR;
# 1 for minimum diversity and 0 for maximum. (Default: 0.5)

# Score Threshold
SCORE_THRESHOLD = 1.0

# Get Final Document Object
documents = get_final_document(FOLDERPATH, True)
# print(documents)

# Create Embeddings
embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
)

# Create Vector Store
vector_store = Chroma(
    collection_name="characters_collection",
    embedding_function=embeddings,
    persist_directory=PERSIST_DIRECTORY,  # Where to save data locally, remove if not necessary
)

# Log data for DEBUG
logger.debug("Folder Path: %s", FOLDERPATH)
logger.debug("Embedding Model: %s", EMBEDDING_MODEL)
logger.debug("Persist Directory: %s", PERSIST_DIRECTORY)
logger.debug("Number of results (k): %s", NUM_RESULTS)
logger.debug("Diversity of Retriever: %s", MMR_DIVERSITY)
logger.debug("Score Threshold: %s", SCORE_THRESHOLD)
logger.debug("Documents: %s", documents)

# Define MMR Retriever
retriever = vector_store.as_retriever(
    search_type="mmr",
    # search_type = "similarity_score_threshold",
    search_kwargs={"k": NUM_RESULTS, "fetch_k": NUM_RESULTS + 10, "lambda_mult": MMR_DIVERSITY, 'score_threshold': SCORE_THRESHOLD},
)


# Clear Vector Store
def clear_vector_store():
    try:
        shutil.rmtree(PERSIST_DIRECTORY)
        logger.info("Vector Store has been cleared. Located at %s", PERSIST_DIRECTORY)
    except Exception as e:
        logger.error("Error clearing Vector Store: %s", e)

# Query Vector Store (Similarity Search)
def query_vector_store(query: str) -> list[Document]:
    return vector_store.similarity_search(query, k=NUM_RESULTS)


# Query Vector Store (Similarity Search with Score)
def query_vector_store_with_score(query: str) -> list[tuple[Document, float]]:
    return vector_store.similarity_search_with_score(query, k=NUM_RESULTS)


# Query Vector Store (Vector Search)
def query_vector_store_vector_search(query: str) -> list[Document]:
    return vector_store.similarity_search_by_vector(
        embedding=embeddings.embed_query(query), k=NUM_RESULTS)

# Query Vector Store (as Retriver)
def query_vector_store_as_retriever(query: str) -> list[Document]:
    return retriever.invoke(query)


# Add Document to Vector Store
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)
logger.info("Document(s) added to Vector Store")


# Example Usage
if __name__ == "__main__":
    print("[+] =====>>> Query Vector Store (Similarity Search)")
    print(query_vector_store("What is Phase's Ranged basic attack?"))

    print("[+] =====>>> Query Vector Store (Similarity Search with Score)")
    print(query_vector_store_with_score("What is Phase's Ranged basic attack?"))

    print("[+] =====>>> Query Vector Store (Vector Search)")
    print(query_vector_store_vector_search("What is Phase's Ranged basic attack?"))

    print("[+] =====>>> Query Vector Store (as Retriver)")
    print(query_vector_store_as_retriever("What is Phase's Ranged basic attack?"))
