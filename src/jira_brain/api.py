from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
from jira_brain.rag import answer, RagAnswer

load_dotenv()
client = Anthropic()
app = FastAPI()

class AskRequest(BaseModel):
    question: str

@app.post("/ask", response_model=RagAnswer)
def ask(req: AskRequest):
    return answer(req.question)