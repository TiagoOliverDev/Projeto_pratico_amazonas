import os

from bson.json_util import dumps

from mongo_connection import create_client, get_database_name


def print_collection(db, collection_name: str) -> None:
    print(f"\n===== COLECAO: {collection_name} =====")
    documents = list(db[collection_name].find())

    if not documents:
        print("(sem documentos)")
        return

    for doc in documents:
        print(dumps(doc, indent=2, ensure_ascii=False))


def main() -> None:
    client = create_client(require_primary=False)
    db = client[get_database_name()]

    for name in ["clientes", "produtos", "pedidos", "carrinho", "avaliacoes"]:
        print_collection(db, name)


if __name__ == "__main__":
    main()
