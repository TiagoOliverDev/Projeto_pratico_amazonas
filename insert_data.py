import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from bson.decimal128 import Decimal128

from mongo_connection import create_client, get_database_name


def dec(value: str) -> Decimal128:
    return Decimal128(Decimal(value))


def main() -> None:
    client = create_client(require_primary=True)
    db = client[get_database_name()]
    now = datetime.now(timezone.utc)

    clientes = [
        {
            "_id": "cli-001",
            "nome": "Ana Souza",
            "email": "ana.souza@amazonas.com",
            "enderecos": [
                {
                    "rua": "Rua das Acacias, 100",
                    "cidade": "Manaus",
                    "estado": "AM",
                    "cep": "69000-000",
                    "principal": True,
                }
            ],
            "data_cadastro": now,
        },
        {
            "_id": "cli-002",
            "nome": "Bruno Lima",
            "email": "bruno.lima@amazonas.com",
            "enderecos": [
                {
                    "rua": "Av. Brasil, 2500",
                    "cidade": "Sao Paulo",
                    "estado": "SP",
                    "cep": "01000-000",
                    "principal": True,
                }
            ],
            "data_cadastro": now,
        },
    ]

    produtos = [
        {
            "_id": "prd-001",
            "nome": "Notebook X15",
            "preco": dec("4299.90"),
            "categoria": "Eletronicos",
            "estoque": 50,
            "avaliacao_media": 4.7,
        },
        {
            "_id": "prd-002",
            "nome": "Fone Bluetooth Pro",
            "preco": dec("299.99"),
            "categoria": "Eletronicos",
            "estoque": 140,
            "avaliacao_media": 4.4,
        },
        {
            "_id": "prd-003",
            "nome": "Cafeteira Premium",
            "preco": dec("389.50"),
            "categoria": "Casa",
            "estoque": 75,
            "avaliacao_media": 4.2,
        },
    ]

    pedidos = [
        {
            "_id": "ped-001",
            "cliente_id": "cli-001",
            "status": "Pago",
            "valor_total": dec("4599.89"),
            "itens": [
                {
                    "produto_id": "prd-001",
                    "nome": "Notebook X15",
                    "preco_epoca": dec("4299.90"),
                    "quantidade": 1,
                },
                {
                    "produto_id": "prd-002",
                    "nome": "Fone Bluetooth Pro",
                    "preco_epoca": dec("299.99"),
                    "quantidade": 1,
                },
            ],
            "endereco_entrega_snapshot": {
                "rua": "Rua das Acacias, 100",
                "cidade": "Manaus",
                "estado": "AM",
                "cep": "69000-000",
            },
        },
        {
            "_id": "ped-002",
            "cliente_id": "cli-002",
            "status": "Enviado",
            "valor_total": dec("389.50"),
            "itens": [
                {
                    "produto_id": "prd-003",
                    "nome": "Cafeteira Premium",
                    "preco_epoca": dec("389.50"),
                    "quantidade": 1,
                }
            ],
            "endereco_entrega_snapshot": {
                "rua": "Av. Brasil, 2500",
                "cidade": "Sao Paulo",
                "estado": "SP",
                "cep": "01000-000",
            },
        },
    ]

    carrinho = [
        {
            "_id": "car-001",
            "cliente_id": "cli-001",
            "itens": [
                {"produto_id": "prd-003", "quantidade": 1},
                {"produto_id": "prd-002", "quantidade": 2},
            ],
            "atualizado_em": now - timedelta(hours=1),
        }
    ]

    avaliacoes = [
        {
            "_id": "avl-001",
            "produto_id": "prd-001",
            "nota": 5,
            "comentario": "Excelente desempenho para trabalho e jogos.",
        },
        {
            "_id": "avl-002",
            "produto_id": "prd-002",
            "nota": 4,
            "comentario": "Bom custo-beneficio e bateria duradoura.",
        },
    ]

    for doc in clientes:
        db.clientes.replace_one({"_id": doc["_id"]}, doc, upsert=True)
    for doc in produtos:
        db.produtos.replace_one({"_id": doc["_id"]}, doc, upsert=True)
    for doc in pedidos:
        db.pedidos.replace_one({"_id": doc["_id"]}, doc, upsert=True)
    for doc in carrinho:
        db.carrinho.replace_one({"_id": doc["_id"]}, doc, upsert=True)
    for doc in avaliacoes:
        db.avaliacoes.replace_one({"_id": doc["_id"]}, doc, upsert=True)

    print("Dados inseridos/atualizados com sucesso.")


if __name__ == "__main__":
    main()
