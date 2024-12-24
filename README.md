# Echo Whisper

Echo Whisper is an AI assistant that uses a locally hosted Large Language Model (LLM) to power NPC conversations in Unreal Engine! Each NPC can be designed with its own personality and backstory, all driven by simple documents that guide their dialogue. While smaller LLMs come with their challenges, this is just the beginning of what’s possible.

## Tech Stack:

* Ollama: For serving the LLM locally
* LangChain: For LLM query management and Retrieval-Augmented Generation (RAG)
* Chroma DB: Vector database for efficient storage and retrieval
* FastAPI: Handling communication between the LLM and Unreal Engine

## Installation:

1. Clone the repository: 

```bash
git clone https://github.com/archangel4031/EchoWhisperAPI.git
```

2. Install Python from [here](https://www.python.org/downloads/release/python-3124/). It will install `Python Version 3.12.4`. You do not need to install it if you plan to use *Anaconda*.

3. Install the Ollama from [here](https://ollama.com/download)

4. Install the Ollama Models with following commands:

```bash
ollama pull llama3.2:1b-instruct-q4_K_S
ollama pull nomic-embed-text:latest
```

You can use other models available from [Ollama's Models Page](https://ollama.com/search)

5. You may need to install Microsoft C++ Build Tools from [here](https://visualstudio.microsoft.com/downloads/?q=build+tools). This is required by some packages like chroma-hnswlib

### Installation of Environment via `uv` (Recommended):

<details>
<summary>Click to expand</summary>

#### 1. Install the `uv` package:

```bash
pip install uv
```

#### 2. Create *uv* Virtual Environment:

Navigate to the folder containing the `EchoWhisperAPI` folder and run the following command:

```bash
uv venv echowhisper
```

#### 3. Activate the environment:

```bash
.\echowhisper\Scripts\activate
```

#### 4. Install the requirements:

```bash
uv pip install -r requirements.txt
```

#### 5. (Optional) Install Python Magic Package:

Sometimes `python-magic` library fails to install properly. Use the following commadn to install it:

```bash
uv pip install python-magic python-magic-bin --force-reinstall
```

</details>

### Installation of Environment via `Anaconda`:

<details>
<summary>Click to expand</summary>

#### 1. Install the Anaconda Environment:

```bash
conda env create -n echowhisper -f _conda\EchoWhisper_conda.yml 
```

#### 2. Activate the environment (Using Anaconda Terminal):

```bash
conda activate echowhisper
```

</details>

## Running the Server:

- Run the FastAPI server:

```bash
python .\EchoWhisper_Main_v1.py
```

- You can set logging level with the following command:

```bash
python .\EchoWhisper_Main_v1.py --log-level DEBUG
```

## Usage:

You can verify the server is running by opening your web browser and navigating to http://localhost:8081. You can then make API requests to the server using the FastAPI endpoint.

### Endpoints:

Chat endpoint is served at

```bash 
http://localhost:8081/chat
```

### Example Request:

After the FastAPI Server is successfully running, run this from a terminal to verify the server is running and responding:

```bash
curl -X POST "http://127.0.0.1:8081/chat" -H "Content-Type: application/json" -d '{"user_query": "How are you Phase?"}'
```

### Unreal Engine Integration:

A sample template along with API for Unreal Engine 5.5.1 is provided in the [Echo Whisper Template on MEGA](https://mega.nz/folder/D5IEhaZT#PIEDeyTS19-9I8YHkDKAZA).
*Poor me cannot afford paid GitHub Storage yet*

### Adding your own Documents:

You can add your own documents to the vector store by creating a **Markdown File** file in the *EchoWhisperAPI/docs* folder. Make sure to delete the Vector Store and restart the server after adding new documents.

## Video Demo:

A video demo is available here on [YouTube](https://www.youtube.com)

## Todo:

- [X] Replace Anaconda with `uv`
- [ ] Add Chat History
- [ ] Add Conversation Memory per NPC
- [ ] Support for more document formats (PDF, docx, etc.)
- [ ] Add document filters in requests to the LLM
- [ ] Add Docker Support (in addition to local installation)
- [ ] Add Colab Support (via ngrok)
- [ ] Add support for CPU LLM Models (BitNet)
- [ ] Add RPG Elements (e.g. Quest Tracking, Inventory, Stats, etc.)