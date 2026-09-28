import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

class RagAnswer(BaseModel):
    answer: str
    sources: list[str]
    confidence: float


load_dotenv()
client = Anthropic()
db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_or_create_collection("tickets")


def retrieve(question: str, k: int = 3) -> list[dict]:
    results = collection.query(query_texts=[question], n_results=k)
    return [
        {"key": key, "text": doc, "distance": dist}
        for key, doc, dist in zip(
            results["ids"][0], results["documents"][0], results["distances"][0]
        )
    ]


def answer(question: str) -> RagAnswer:
    tickets = retrieve(question)
    context = "\n\n".join(f"[{t['key']}]\n{t['text']}" for t in tickets)

    system = (
        "You answer questions about Jira tickets. Use only the tickets provided. "
        "Put the ticket keys you relied on in sources, e.g. PROJ-101. "
        "If the tickets don't contain the answer, say so, leave sources empty, "
        "and set confidence low. Confidence is 0.0 to 1.0."
    )
    user = f"Tickets:\n\n{context}\n\nQuestion: {question}"

    resp = client.messages.parse(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_format=RagAnswer,
    )
    return resp.parsed_output


if __name__ == "__main__":
    import sys
    result = answer(" ".join(sys.argv[1:]))
    print(result.model_dump_json(indent=2))