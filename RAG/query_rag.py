from os import pardir
import json
import os

from chromadb.types import Segment
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TQDM_DISABLE", "1")

import chromadb
from chromadb.utils import embedding_functions


def main():
    db_storage_path = "./Knowledge/ChromaDB_Storage/"

    chroma_client = chromadb.PersistentClient(path=db_storage_path)

    hf_embed = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2",
    )

    collection = chroma_client.get_or_create_collection(
        name="Epub-Library", embedding_function=hf_embed
    )

    user_query = input("Enter you Query: ")

    print(f"Retriving Data from User Query {user_query}")

    result = collection.query(query_texts=[user_query], n_results=4)

    ids = result["ids"][0]
    docs = result["documents"][0]
    metadts = result["metadatas"][0]
    ans = ""

    contexts = []
    for i, id in enumerate(ids):
        doc = docs[i]
        ans += doc
        ans += "\n"
        metadt = metadts[i]

        context = {
            "ID": id,
            "Souce": metadt["source"],
            "Chapter": metadt["chapter"],
            "Segment": metadt["segment"],
            "Text": doc,
        }
        contexts.append(context)

        with open("contexts.json", "w") as f:
            json.dump(contexts, f, indent=1)

        print("\n===================================")
        print("ID:", id)
        print("source:", metadt["source"])
        print("Chapter:", metadt["chapter"])
        print("Segment:", metadt["segment"])
        print("------------------------------------")
        print("Answer:", doc)
        print("__________\n")

        print("OVERALL ANSWER:")

    print(ans)


if __name__ == "__main__":
    main()
