# Legal RAG Agent API

> An autonomous AI agent for legal contract analysis built on a state graph architecture.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-LangChain-1C3C3C?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-Google_AI-4285F4?style=flat-square&logo=google&logoColor=white)

---

## Project Description

This project implements a corporate RESTful API that acts as an AI Agent specialized in legal contract analysis.

Unlike traditional linear RAG (Retrieval-Augmented Generation) pipelines, this system uses a State Graph architecture (LangGraph) to give the LLM logical autonomy. The agent acts as a strict auditor, evaluating the relevance of retrieved documents before generating a response and actively blocking hallucinations when the requested information is not present in the knowledge base.

The system includes a batch ingestion pipeline with metadata processing, enabling hybrid searches (vector similarity + SQL-like filters), and is fully containerized for production deployment.

---

## Architecture and Technologies

- **Primary Language:** Python 3.11+
- **API Framework:** FastAPI and Uvicorn
- **Agent Orchestration:** LangChain and LangGraph
- **Vector Database:** ChromaDB (Local)

### AI Models

- **Embeddings:** HuggingFace (Open-source)
- **LLM:** Google Gemini 2.5 Flash

### Infrastructure

- Docker

### Quality and Testing

- Pytest
- Python native logging

---

## Project Structure

```plaintext
.
├── chroma_db/               # Persistent vector database (auto-generated)
├── dados/                   # Source directory for raw PDF files
├── src/                     # Main source code
│   ├── agent/               # Autonomous Agent logic
│   │   ├── graph.py         # LangGraph flow definition (Routing)
│   │   ├── nodes.py         # Execution functions (Retrieval, Evaluation, Generation)
│   │   └── state.py         # Global agent state definition
│   ├── database/            # Data Pipeline and Persistence
│   │   ├── chroma_client.py # Vector database connection and configuration
│   │   └── ingestion.py     # Batch processing script and metadata extraction
│   └── main.py              # API entry point and route configuration
├── tests/                   # Automated test suite
│   ├── __init__.py
│   └── test_api.py          # Integration tests for the main route
├── .env                     # Environment variables (not versioned)
├── .dockerignore            # Exclusion rules for Docker image build
├── Dockerfile               # Infrastructure recipe for containerization
└── requirements.txt         # Project dependencies
```

---

## Agent Logic Flow (LangGraph)

The API's cognitive processing follows three strict evaluation steps.

### 1. Retrieval Node

Performs a hybrid search in ChromaDB, combining:

- Vector similarity of the question
- Metadata extracted during the ingestion pipeline

Metadata examples:

- Contract status
- Document type
- Legal category

---

### 2. Evaluation Node (Grade Documents)

The LLM acts as an internal judge.

It receives the retrieved fragments and evaluates, in a binary manner (yes/no), whether the texts contain sufficient information to answer the question.

- Useful fragments are approved
- Irrelevant fragments are discarded

---

### 3. Generation Node

Receives only the context approved in the previous step.

#### Possible scenarios

**If valid context exists:**
The agent formulates a structured legal response.

**If context is empty:**
The safety lock is triggered and the system returns that the information is not present in the knowledge base.

---

## Running Locally (Development Environment)

### Prerequisites

- Python 3.11 or higher
- Google AI Studio account for API key generation

---

### Installation and Setup

Clone the repository:

```bash
git clone https://github.com/1Pereira/Agente-RAG-juridico.git
cd Agente-RAG-juridico
```

Create and activate a virtual environment:

**Windows**

```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux/macOS**

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_key_here
```

---

### Data Ingestion

Add your `.pdf` files inside the `dados/` folder.

Then run the ingestion pipeline:

```bash
cd src/database
python ingestion.py
```

The script will:

- Process the PDFs
- Extract metadata
- Generate embeddings
- Populate ChromaDB

---

### Starting the API

Return to the project root:

```bash
cd ../..
python src/main.py
```

The API will be available at:

```plaintext
http://localhost:8000
```

---

## Running via Docker (Production Environment)

The project includes a configured `Dockerfile` for isolated and reproducible execution.

### Building the image

```bash
docker build -t agente-rag-api .
```

### Running the container

```bash
docker run -p 8000:8000 --env-file .env agente-rag-api
```

---

## API Reference

### Main Endpoint

#### `POST /perguntar`

**Request body**

```json
{
  "pergunta": "What is the termination penalty percentage?"
}
```

**Example response**

```json
{
  "pergunta": "What is the termination penalty percentage?",
  "resposta": "The termination penalty described in the service agreement is 5% of the total remaining contract value."
}
```

---

### Swagger UI

Interactive documentation is available at:

```plaintext
http://localhost:8000/docs
```

---

## Test Suite

The project uses `pytest` to validate routes and API behavior.

Tests simulate:

- Complete HTTP requests
- JSON output validation
- Response time
- Integrity of returned keys

### Running the tests

```bash
pytest -q --disable-warnings
```

---

## Monitoring and Logs

The application has a native logging system configured.

The following events are recorded:

- Incoming requests
- LangGraph node transitions
- Critical infrastructure errors
- Handled exceptions via `try/except`

### Log outputs

- Real-time console output
- Persistent log file:

```plaintext
app.log
```

This enables traceability, auditing and operational monitoring of the agent.

---

## Technical Highlights

- Autonomous agent architecture
- LLM hallucination protection
- Hybrid vector + metadata search
- Automated ingestion pipeline
- Local vector persistence
- Corporate RESTful API
- Docker containerization
- Modular and scalable structure
- Logging and observability
- Automated testing