from pathlib import Path
import chromadb

db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_or_create_collection("tickets")

for f in Path("data/tickets").glob("*.md"):
    text = f.read_text(encoding="utf-8")
    collection.add(
        ids=[f.stem],
        documents=[text],
        metadatas=[{"key": f.stem}],
    )
    print("added", f.stem)
