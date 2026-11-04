# Supply chain

A small Python tutorial project for experimenting with LangChain, LangGraph, Ollama, and Neo4j in a supply-chain question-answering workflow.

## Project structure

- `supply-chain/simple_agent.py` — a minimal LangGraph agent that retrieves sample weather context and generates an answer with Ollama.
- `supply-chain/cypher_qa.py` — a Neo4j graph QA example that generates and runs a Cypher query for a supply-chain question.
- `supply-chain/test_environment.py` — checks the `.env` file and, when configured, the Ollama and Neo4j connections.
- `conftest.py` — shared pytest helpers and automatic `.env` loading.

## Requirements

- Python 3.10 or newer
- Ollama running locally with a chat model available, such as `llama3.2`
- Neo4j running locally or a reachable Neo4j instance for the graph QA example

## Setup

Create and activate a virtual environment, then install the pinned dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Copy the environment template and fill in the connection details:

```bash
cp .env.example .env
```

The application reads these variables from `.env`:

```dotenv
OLLAMA_MODEL=llama3.2
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j
```

`OPENAI_API_KEY` is included in the environment template for related experiments, but the current examples use Ollama.

## Run the examples

From the project root:

```bash
python supply-chain/simple_agent.py
python supply-chain/cypher_qa.py
```

The graph QA example expects a populated Neo4j database with the supply-chain labels, relationships, and properties referenced in its Cypher prompt.

## Run the tests

```bash
pytest
```

The environment tests are skipped when the required `.env` values are unavailable. When configured, they verify the Ollama and Neo4j connections as well.

## Notes

- Do not commit `.env`; it is ignored by Git.
- The examples are intended for learning and experimentation. Review generated Cypher before using it against a production database.
