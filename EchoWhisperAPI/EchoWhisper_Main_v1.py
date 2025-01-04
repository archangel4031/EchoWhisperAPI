from modules.customLogger import setup_logger, set_log_level
import argparse
logger = setup_logger()

# Parse command-line arguments to get log level
parser = argparse.ArgumentParser(description="Custom Logger Setup")
parser.add_argument(
    "--log-level",
    type=str.upper,
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default="WARNING",
    help="Set the log level (default: INFO)",
)
args = parser.parse_args()

# Create a logger with a specific name
set_log_level(args.log_level)


from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from modules.llm_query import query_llm_with_limited_memory
from modules.vector_store_retriever import query_vector_store_with_score, clear_vector_store


# Clear Vector Store (use this if settings have changed in vector_store_retriever.py OR doc_loader_splitter_md.py)
# clear_vector_store()

# Create the FastAPI app
app = FastAPI()

# Class for handling chat requests and responses
class ChatRequest(BaseModel):
    user_query: str
    system_instruction: Optional[str] = None  # Optional system instruction
    document_query: Optional[str] = None  # Optional document query

class ChatResponse(BaseModel):
    response: str
    metadata: str = ""  # Empty for now


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serves the root HTML page of the Echo Whisper API application.

    Returns:
        HTMLResponse: A simple HTML page providing information about
        the Echo Whisper API, including its status and available endpoints.
    """

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Echo Whisper</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
                line-height: 1.6;
            }
            header {
                background: #333;
                color: #fff;
                padding: 10px 0;
                text-align: center;
            }
            h1 {
                margin: 20px 0;
            }
            p {
                margin: 10px 0;
            }
            a {
                color: #007BFF;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .container {
                width: 80%;
                margin: 20px auto;
                padding: 20px;
                background: #fff;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Echo Whisper API</h1>
        </header>
        <div class="container">
            <p>App is active</p>
            <p>Chat endpoint: <a href="/chat">/chat</a></p>
            <p>Example with curl (run this in a separate terminal):</p>
            <pre><code>curl -X POST "http://127.0.0.1:8081/chat" \
-H "Content-Type: application/json" \
-d '{"user_query": "How are you Phase?"}'</code></pre>
        </div>
    </body>
    </html>
    """
    return html_content

@app.post("/chat")
async def chat(req: ChatRequest):
    """
    Endpoint to send a message to the LLM and receive a response.
    Input: ChatRequest = {user_query: str, system_instruction: Optional[str], document_query: Optional[str]}
    Output: ChatResponse = {response: str, metadata: str}
    """
    document_content = ""

    # Log received ChatRequest
    logger.info("New Request Received")
    logger.debug("Received ChatRequest: %s", req)
    logger.debug("User Query: %s", req.user_query)
    logger.debug("System Instruction: %s", req.system_instruction)
    logger.debug("Document Query: %s", req.document_query)

    if not req.document_query:
        # Pass the user query for a retriever query search
        documents = query_vector_store_with_score(req.user_query)
    else:
        # Pass the document query for a vector search
        documents = query_vector_store_with_score(req.document_query)

    # Check if the score is less than 1, Set documents to None if less
    if documents:
        for doc, score in documents:
            logger.debug("Document Score: %s", score)
            if score < 1:  # Lower score represents more similarity.
                document_content += doc.page_content
            else:
                document_content = ""
                break
    else:
        document_content = ""

    logger.debug("Document Content: %s", document_content)

    # Use LangChain and Ollama to process the request
    try:
        # Get the response from the LLM
        llm_response = query_llm_with_limited_memory(
            req.user_query,
            document_content,
            req.system_instruction
        )

        logger.info("LLM Response Received")
        logger.debug("LLM Response: %s", llm_response)

        return ChatResponse(response=llm_response.content)

    except Exception as e:
        logger.error("Error processing request: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8081)
