from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Define request schema
class ChatRequest(BaseModel):
    query: str

# Set up Groq LLM
llm = ChatGroq(
    temperature=0.7,
    model_name="Gemma2-9b-it",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Define prompt template
prompt = PromptTemplate.from_template("You are a helpful assistant. Answer this: {query}")

# Set up LangChain Expression Language Chain (LELC-like structure)
chain = prompt | llm | StrOutputParser()

@app.post("/chat")
async def chat(request: ChatRequest):
    response =  chain.invoke({"query": request.query})
    return {"response": response}
