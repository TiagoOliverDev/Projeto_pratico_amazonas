FROM mongo:7.0

# Scripts used to bootstrap the replica set and initialize the schema.
COPY mongo-init/init.js /scripts/init.js
COPY scripts/init-replica.sh /scripts/init-replica.sh

RUN chmod +x /scripts/init-replica.sh
