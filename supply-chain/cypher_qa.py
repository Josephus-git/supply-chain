import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts.prompt import PromptTemplate
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph

# Initialize the LLM using Ollama
ollama_model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
model = init_chat_model(ollama_model_name, model_provider="ollama")

# Connect to Neo4j graph database
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE"),
)

# Enhanced Cypher prompt containing your manual query as a few-shot example
cypher_template = """Task: Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Examples:

# Example 1: Find products, suppliers, departure, and arrival ports based on a product type and departure port
Question: Find suppliers for products similar to vacuum cleaner departing from Tanjung Pelepas.
Cypher:
MATCH (node:Product)<-[:CONTAINS_PRODUCT]-(shipment:Shipment)
MATCH (supplier:Supplier)-[:SHIPPED]->(shipment)
MATCH (shipment)-[:DEPARTED_FROM]->(exit_port)
WHERE toLower(coalesce(exit_port.exit_port, "")) CONTAINS toLower("Tanjung Pelepas")
OPTIONAL MATCH (shipment)-[:ARRIVED_AT]->(entry_port)
RETURN
    node.product_description AS product_description,
    node.full_hs_code_description AS full_hs_code_description,
    supplier.supplier_name AS supplier,
    exit_port.exit_port AS departure_port,
    collect(DISTINCT entry_port.entry_port) AS arrival_ports,
    count(DISTINCT shipment) AS shipment_count
ORDER BY shipment_count DESC

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""

cypher_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_template
)

# Create the Cypher QA chain with the updated prompt
cypher_qa = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=model,
    cypher_llm=model,
    cypher_prompt=cypher_prompt,
    allow_dangerous_requests=True,
    verbose=True,
)

# Invoke the chain with a target question
question = "Find suppliers for products similar to vacuum cleaner departing from Tanjung Pelepas"
response = cypher_qa.invoke({"query": question})

print("\n--- Final Answer ---")
print(response["result"])