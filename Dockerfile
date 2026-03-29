FROM mongo:7.0

# Script executed on first container start to initialize database and indexes.
COPY mongo-init/init.js /docker-entrypoint-initdb.d/01-init.js
