#!/bin/bash
set -euo pipefail

echo "Aguardando nos do MongoDB responderem..."
for attempt in {1..30}; do
  if mongosh --host mongo1:27017 --quiet --eval "db.adminCommand('ping').ok" >/dev/null 2>&1 \
    && mongosh --host mongo2:27017 --quiet --eval "db.adminCommand('ping').ok" >/dev/null 2>&1 \
    && mongosh --host mongo3:27017 --quiet --eval "db.adminCommand('ping').ok" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

echo "Inicializando replica set rs0..."
mongosh --host mongo1:27017 --quiet <<'EOF'
try {
  rs.status();
  print("Replica set ja inicializado.");
} catch (error) {
  rs.initiate({
    _id: "rs0",
    members: [
      { _id: 0, host: "mongo1:27017", priority: 2 },
      { _id: 1, host: "mongo2:27017", priority: 1 },
      { _id: 2, host: "mongo3:27017", priority: 1 }
    ]
  });
}
EOF

echo "Aguardando eleicao do no primario..."
for attempt in {1..30}; do
  if mongosh --host mongo1:27017 --quiet --eval "db.hello().isWritablePrimary" | grep -q "true"; then
    break
  fi
  sleep 2
done

echo "Criando banco, colecoes e indices..."
mongosh "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/admin?replicaSet=rs0" /scripts/init.js

echo "Replica set e schema configurados com sucesso."