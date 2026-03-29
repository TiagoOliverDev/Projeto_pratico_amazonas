import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError


DEFAULT_HOSTS = ["localhost:27017", "localhost:27018", "localhost:27019"]


def get_database_name() -> str:
    return os.getenv("MONGO_DB", "amazonas_ecommerce")


def create_client(require_primary: bool = False) -> MongoClient:
    custom_uri = os.getenv("MONGO_URI")
    if custom_uri:
        client = MongoClient(custom_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client

    last_error = None
    for host in DEFAULT_HOSTS:
        client = MongoClient(
            f"mongodb://{host}/?directConnection=true",
            serverSelectionTimeoutMS=5000,
        )
        try:
            hello = client.admin.command("hello")
            if require_primary and not hello.get("isWritablePrimary", False):
                client.close()
                continue
            return client
        except (PyMongoError, ServerSelectionTimeoutError) as error:
            last_error = error
            client.close()

    if last_error is not None:
        raise last_error

    raise RuntimeError("Nenhum no MongoDB disponivel foi encontrado.")
