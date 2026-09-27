from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
app = FastAPI()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": req.question}],
    )
    return AskResponse(answer=resp.content[0].text)