# Projeto MongoDB E-commerce Amazonas

Este projeto sobe um cluster MongoDB local com replica set de 3 nos para atender ao requisito de replicacao e alta disponibilidade da modelagem proposta.

O ambiente inclui:

- 1 no primario eleito automaticamente;
- 2 nos secundarios;
- failover automatico do replica set;
- criacao automatica do banco `amazonas_ecommerce`;
- scripts Python para inserir e consultar dados.

## Estrutura

- `Dockerfile`: imagem customizada usada pelos containers MongoDB.
- `docker-compose.yml`: sobe `mongo1`, `mongo2`, `mongo3` e o container de bootstrap do replica set.
- `mongo-init/init.js`: cria banco, colecoes e indices.
- `scripts/init-replica.sh`: inicializa o replica set e aplica o schema.
- `insert_data.py`: insere ou atualiza dados de exemplo.
- `query_all_data.py`: lista todos os documentos de todas as colecoes.
- `requirements.txt`: dependencias Python.

## Pre-requisitos

- Docker Desktop instalado e em execucao.
- Python 3.10 ou superior.
- PowerShell no Windows.

## Como rodar no Windows/PowerShell

1. Abra o Docker Desktop e espere o status `Engine running`.

2. Entre na pasta do projeto:

```powershell
cd "C:\Projeto_pratico_amazonas"
```

3. Suba o cluster MongoDB:

```powershell
docker compose up -d --build
```

4. Verifique os containers em execucao:

```powershell
docker ps
```

Voce deve ver estes containers principais:

- `amazonas-mongo1`
- `amazonas-mongo2`
- `amazonas-mongo3`

O container `amazonas-mongo-setup` executa a configuracao do replica set e pode finalizar logo depois. Isso e esperado.

5. Confira os logs da inicializacao do replica set:

```powershell
docker logs amazonas-mongo-setup
```

Se a configuracao tiver sido concluida, os logs mostrarao que o replica set e o schema foram aplicados com sucesso.

6. Crie e ative um ambiente virtual Python:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

7. Instale as dependencias Python:

```powershell
pip install -r requirements.txt
```

8. Insira os dados de exemplo:

```powershell
python insert_data.py
```

9. Consulte todos os dados:

```powershell
python query_all_data.py
```

## URI padrao dos scripts Python

Se voce definir `MONGO_URI`, os scripts usarao exatamente essa conexao.

Se voce nao definir `MONGO_URI`, os scripts tentam se conectar automaticamente nas portas publicadas do Docker no host:

```text
localhost:27017
localhost:27018
localhost:27019
```

Nesse modo, o script de insercao detecta qual porta corresponde ao no primario e grava os dados nele. O script de consulta usa o primeiro no disponivel.

Esse comportamento foi necessario porque o replica set anuncia nomes internos do Docker (`mongo1`, `mongo2`, `mongo3`), que nao sao resolvidos diretamente pelo Windows host.

## Variaveis de ambiente opcionais

- `MONGO_URI`
- `MONGO_DB`

Exemplo no PowerShell:

```powershell
$env:MONGO_URI = "mongodb://localhost:27017/?directConnection=true"
$env:MONGO_DB = "amazonas_ecommerce"
python query_all_data.py
```

## Validar replicacao e alta disponibilidade

Ver status do replica set:

```powershell
docker exec -it amazonas-mongo1 mongosh --eval "rs.status()"
```

Ver qual no e o primario:

```powershell
docker exec -it amazonas-mongo1 mongosh --eval "db.hello()"
```

Simular failover parando o no primario:

```powershell
docker stop amazonas-mongo1
```

Depois consulte novamente o status por outro no:

```powershell
docker exec -it amazonas-mongo2 mongosh --eval "rs.status()"
```

## Recriar o ambiente do zero

Se quiser apagar os volumes e reconstruir tudo:

```powershell
docker compose down -v
docker compose up -d --build
```

## Problemas comuns

### Docker Desktop desligado

Se aparecer erro como este:

```text
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified
```

O Docker Desktop nao esta ativo. Abra o programa, espere o engine iniciar e rode novamente:

```powershell
docker compose up -d --build
```

### Replica set ainda inicializando

Se os scripts Python falharem logo apos o `docker compose up`, aguarde alguns segundos e verifique:

```powershell
docker logs amazonas-mongo-setup
```

Depois execute novamente:

```powershell
python insert_data.py
python query_all_data.py
```

### Erro `getaddrinfo failed` com `mongo1`, `mongo2` ou `mongo3`

Se aparecer erro informando que `mongo1`, `mongo2` ou `mongo3` nao foram encontrados, isso significa que o cliente Python no Windows tentou usar os nomes internos da rede Docker.

Os scripts ja foram ajustados para evitar isso automaticamente quando `MONGO_URI` nao esta definida.

Se voce definiu `MONGO_URI` manualmente, use uma conexao direta por porta publicada, por exemplo:

```powershell
$env:MONGO_URI = "mongodb://localhost:27017/?directConnection=true"
python insert_data.py
```

## Observacoes

- O indice TTL da colecao `carrinho` remove documentos apos 48 horas (`172800` segundos).
- Este ambiente atende o requisito de replica set com 3 nos para laboratorio e demonstracao.
- Em producao, seria necessario adicionar autenticacao, segregacao entre hosts, monitoramento, backup e seguranca operacional.
