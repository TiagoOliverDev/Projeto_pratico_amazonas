const dbName = "amazonas_ecommerce";
const ecommerceDb = db.getSiblingDB(dbName);

function createCollectionIfMissing(collectionName) {
  const exists = ecommerceDb.getCollectionNames().includes(collectionName);
  if (!exists) {
    ecommerceDb.createCollection(collectionName);
  }
}

createCollectionIfMissing("clientes");
createCollectionIfMissing("produtos");
createCollectionIfMissing("pedidos");
createCollectionIfMissing("carrinho");
createCollectionIfMissing("avaliacoes");

ecommerceDb.clientes.createIndex({ email: 1 }, { unique: true, name: "idx_clientes_email_unique" });
ecommerceDb.produtos.createIndex({ categoria: 1 }, { name: "idx_produtos_categoria" });
ecommerceDb.pedidos.createIndex({ cliente_id: "hashed" }, { name: "idx_pedidos_cliente_id_hashed" });
ecommerceDb.avaliacoes.createIndex({ produto_id: 1 }, { name: "idx_avaliacoes_produto_id" });
ecommerceDb.carrinho.createIndex(
  { atualizado_em: 1 },
  { expireAfterSeconds: 172800, name: "idx_carrinho_ttl_48h" }
);

print(`Banco '${dbName}' inicializado com sucesso.`);
