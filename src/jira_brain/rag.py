import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

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


def answer(question: str) -> str:
    tickets = retrieve(question)
    context = "\n\n".join(f"[{t['key']}]\n{t['text']}" for t in tickets)

    system = (
        "You answer questions about Jira tickets. Use only the tickets provided. "
        "Cite ticket keys like [PROJ-101]. If the tickets don't contain the answer, say so."
    )
    user = f"Tickets:\n\n{context}\n\nQuestion: {question}"

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


if __name__ == "__main__":
    import sys
    print(answer(" ".join(sys.argv[1:])))