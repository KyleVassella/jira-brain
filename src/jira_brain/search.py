import sys
import chromadb

db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_or_create_collection("tickets")

question = " ".join(sys.argv[1:])
results = collection.query(query_texts=[question], n_results=3)

for key, doc, dist in zip(results["ids"][0], results["documents"][0], results["distances"][0]):
    print(f"\n[{key}]  distance={dist:.3f}\n{doc[:200]}")
