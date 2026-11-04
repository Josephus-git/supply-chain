import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

# Initialize the LLM using the model name defined in your .env (OLLAMA_MODEL)
ollama_model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
model = init_chat_model(ollama_model_name, model_provider="ollama")

# Create a prompt
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}

Answer:"""

prompt = PromptTemplate.from_template(template)


# Define state for application
class State(TypedDict):
  question: str
  context: List[dict]
  answer: str


# Define functions for each step in the application


# Retrieve context
def retrieve(state: State):
  context = [
      {"location": "London", "weather": "Cloudy, sunny skies later"},
      {"location": "San Francisco", "weather": "Sunny skies, raining overnight."},
      {"location": "Hull", "weather": "Pink weather"}
  ]
  return {"context": context}


# Generate the answer based on the question and context
def generate(state: State):
  messages = prompt.invoke(
      {"question": state["question"], "context": state["context"]}
  )
  response = model.invoke(messages)
  return {"answer": response.content}


# Define application steps
workflow = StateGraph(State).add_sequence([retrieve, generate])
workflow.add_edge(START, "retrieve")
app = workflow.compile()

# Run the application
question = "What is the weather in London?"
response = app.invoke({"question": question})
print("Answer:", response["answer"])