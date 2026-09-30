import sys
import chromadb
from anthropic import Anthropic, beta_tool
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_or_create_collection("tickets")


@beta_tool
def search_tickets(query: str) -> str:
    """Search Jira tickets by meaning. Returns the 3 most relevant tickets.

    Args:
        query: What to search for, in plain English.
    """
    results = collection.query(query_texts=[query], n_results=3)
    return "\n\n".join(
        f"[{key}]\n{doc}"
        for key, doc in zip(results["ids"][0], results["documents"][0])
    )


@beta_tool
def get_ticket(key: str) -> str:
    """Fetch one Jira ticket by its exact key.

    Args:
        key: The ticket key, e.g. PROJ-101.
    """
    result = collection.get(ids=[key])
    if not result["documents"]:
        return f"No ticket found with key {key}"
    return result["documents"][0]


def run(question: str) -> str:
    runner = client.beta.messages.tool_runner(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=(
            "You answer questions about Jira tickets. Use the tools to look things up. "
            "Cite ticket keys like [PROJ-101]. If you can't find it, say so."
        ),
        tools=[search_tickets, get_ticket],
        messages=[{"role": "user", "content": question}],
    )
    final = None
    for message in runner:
        for block in message.content:
            if block.type == "tool_use":
                print(f"  -> {block.name}({block.input})")
        final = message
    return next(b.text for b in final.content if b.type == "text")


if __name__ == "__main__":
    print(run(" ".join(sys.argv[1:])))