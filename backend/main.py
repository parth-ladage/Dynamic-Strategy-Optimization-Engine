import sys
import os
from pydantic import BaseModel # Import Pydantic for data validation

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.strategy import compare_strategies
from app.services.ai_engineer import ask_gemini_engineer # Import the new service

app = FastAPI(title="F1 Virtual Pit Wall API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class ChatRequest(BaseModel):
    question: str
    strategy_data: dict # The frontend will send the current strategy back to us

@app.get("/")
def read_root():
    return {"status": "Virtual Pit Wall is Online 🟢"}

@app.get("/strategy/optimize")
def get_optimal_strategy():
    try:
        result = compare_strategies()
        return result
    except Exception as e:
        return {"error": str(e)}

# --- NEW ENDPOINT ---
@app.post("/strategy/chat")
def chat_with_engineer(request: ChatRequest):
    """
    Talk to the AI Race Engineer about the current strategy.
    """
    response = ask_gemini_engineer(request.question, request.strategy_data)
    return {"reply": response}