import os

from bson.json_util import dumps
from pymongo import MongoClient


MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin123@localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "amazonas_ecommerce")


def print_collection(db, collection_name: str) -> None:
    print(f"\n===== COLECAO: {collection_name} =====")
    documents = list(db[collection_name].find())

    if not documents:
        print("(sem documentos)")
        return

    for doc in documents:
        print(dumps(doc, indent=2, ensure_ascii=False))


def main() -> None:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    for name in ["clientes", "produtos", "pedidos", "carrinho", "avaliacoes"]:
        print_collection(db, name)


if __name__ == "__main__":
    main()
