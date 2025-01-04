from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json
from typing import Union, List
import os
from modules.customLogger import setup_logger
from modules.load_configs import get_config_value, get_config_object

logger = setup_logger()

# selected_model="llama3.2:latest"
selected_model = "llama3.2:1b-instruct-q4_K_S"
# selected_model="qwen2:0.5b"
selected_model = str(get_config_value(get_config_object(), "LLM Query", "selected_model", selected_model))

# Default System Instruction
DEFAULT_SYSTEM_INSTRUCTION = "You are a Character in a video game. Answer the question in a friendly tone as if you were a real person. Answer briefly and precisely. Format your answer as a continuous string. Reply to greetings properly. Do not make up an answer unless no document context is provided. If you do not know simply reply I dont know the answer to this."
DEFAULT_SYSTEM_INSTRUCTION = str(get_config_value(get_config_object(), "LLM Query", "DEFAULT_SYSTEM_INSTRUCTION", DEFAULT_SYSTEM_INSTRUCTION))

# Chat Messages History Limit
MAX_MESSAGES = 10
MAX_MESSAGES = int(get_config_value(get_config_object(), "LLM Query", "MAX_MESSAGES", MAX_MESSAGES))

# Define the LLM configuration
llm = ChatOllama(
    model=selected_model,
    disable_streaming=True,
    keep_alive=True,
)  # Replace with your Ollama model name

# Initialize chat history
chat_history: List[Union[SystemMessage, HumanMessage, AIMessage]] = []

# File to save the chat history
history_file = "docs/chat_history.json"

# Log data for DEBUG
logger.debug("Selected Model: %s", selected_model)
logger.debug("Default System Instruction: %s", DEFAULT_SYSTEM_INSTRUCTION)
logger.debug("Max Messages: %s", MAX_MESSAGES)
logger.debug("Chat History File: %s", history_file)

# Delete chat history
def delete_chat_history(file_path: str):
    """
    Deletes the chat_history.json file if it exists.

    Parameters:
    - file_path (str): Path to the chat history file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Chat history file deleted.")
    else:
        logger.warning("Chat history file does not exist.")

# Delete chat history Wrapper
def delete_chat_history_wrapper():
    delete_chat_history(history_file)

# Delete chat history on startup
delete_chat_history_wrapper()

# Load chat history from a file
def load_chat_history(
    file_path: str,
) -> List[Union[SystemMessage, HumanMessage, AIMessage]]:
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return [
            (
                SystemMessage(content=msg["content"])
                if msg["role"] == "system"
                else (
                    HumanMessage(content=msg["content"])
                    if msg["role"] == "human"
                    else AIMessage(content=msg["content"])
                )
            )
            for msg in data.get("messages", [])
        ]
    except FileNotFoundError:
        logger.warning("Chat history file not found.")
        return []


# Save chat history to a file
def save_chat_history(
    file_path: str, history: List[Union[SystemMessage, HumanMessage, AIMessage]]
):
    data = {
        "messages": [
            (
                {"role": "system", "content": msg.content}
                if isinstance(msg, SystemMessage)
                else (
                    {"role": "human", "content": msg.content}
                    if isinstance(msg, HumanMessage)
                    else {"role": "ai", "content": msg.content}
                )
            )
            for msg in history
        ]
    }
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Query LLM with memory and limit message history
def query_llm_with_limited_memory(
    user_query: str,
    document_content: str,
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
    chat_history: List[Union[SystemMessage, HumanMessage, AIMessage]] = load_chat_history(history_file),
    max_messages: int = MAX_MESSAGES,
    use_chat_history: bool = False,
) -> str:
    """
    Query the LLM with a system instruction, document content, user query, and limited memory.
    """

    if not system_instruction:
        system_instruction = DEFAULT_SYSTEM_INSTRUCTION

    # Add the system instruction only if starting a new conversation
    if not chat_history and use_chat_history:
        chat_history.append(SystemMessage(content=system_instruction))
        logger.debug("Added System Instruction to Chat History")

    logger.debug("Provided Document Content: %s", document_content)

    # Add context and query to the chat history
    if use_chat_history:
        chat_history.append(HumanMessage(content="Here is some context: " + document_content))
        chat_history.append(HumanMessage(content="Answer this query: " + user_query))
        logger.debug("Added Context and Query to Chat History")

    # Trim the chat history to the last `max_messages`
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]

    # Construct the messages
    if use_chat_history:
        messages = [chat_history[i] for i in range(len(chat_history))] + [
            SystemMessage(content=system_instruction),]
    
    messages = [SystemMessage(content=system_instruction)]
    
    # Add document content message only if document_content is not empty
    if document_content.strip():  # Ensures it’s not empty or just whitespace
        messages.append(HumanMessage(content="Here is some context: " + document_content))

    messages.append(HumanMessage(content="Answer this query: " + user_query))
    
    logger.debug("Constructed Messages: %s", messages)
    logger.debug("Chat History: %s", chat_history)

    # Query the LLM
    logger.info("Querying LLM...")
    response = llm.invoke(messages)

    # Append the User Query and Context to the chat history
    if use_chat_history:
        chat_history.append(HumanMessage(content="Here is some context: " + document_content))
        chat_history.append(HumanMessage(content="Answer this query: " + user_query))

    # Add the model's response to the chat history
    if use_chat_history:
        chat_history.append(AIMessage(content=response.content))

    # Save the updated chat history
    if use_chat_history:
        save_chat_history(history_file, chat_history)

    return response


# Example usage
if __name__ == "__main__":
    document_content = "There is no document context for this query."
    user_query = "What are the best practices for training models?"
    system_instruction = "You are an expert AI assistant."
    response = query_llm_with_limited_memory(user_query, document_content, system_instruction, chat_history)

    print(response)