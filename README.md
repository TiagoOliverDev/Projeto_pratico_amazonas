# Projeto MongoDB E-commerce Amazonas

Este projeto sobe um MongoDB via Docker com inicializacao automatica do banco `amazonas_ecommerce` (colecoes + indices) e inclui scripts Python para:

- inserir dados de exemplo;
- consultar todos os dados.

## Estrutura

- `Dockerfile`: imagem customizada do MongoDB.
- `docker-compose.yml`: orquestra o container do MongoDB.
- `mongo-init/init.js`: cria colecoes e indices (incluindo TTL no carrinho).
- `insert_data.py`: insere/atualiza dados de exemplo em todas as colecoes.
- `query_all_data.py`: consulta e imprime todos os documentos.
- `requirements.txt`: dependencias Python.

## Pre-requisitos

- Docker Desktop instalado e em execucao.
- Python 3.10+ instalado.
- PowerShell (Windows).

## Como rodar (Windows/PowerShell)

1. Abra o Docker Desktop e espere ficar com status `Engine running`.

2. No PowerShell, entre na pasta do projeto:

```powershell
cd "C:\Projeto_pratico_amazonas"
```

3. Suba o MongoDB:

```powershell
docker compose up -d --build
```

4. Confirme se o container ficou ativo:

```powershell
docker ps
```

Voce deve ver o container `amazonas-mongodb` com a porta `27017` exposta.

5. (Opcional, recomendado) Crie e ative um ambiente virtual Python:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

6. Instale as dependencias:

```powershell
pip install -r requirements.txt
```

7. Insira os dados:

```powershell
python insert_data.py
```

8. Consulte todos os dados:

```powershell
python query_all_data.py
```

## Variaveis de ambiente opcionais

Padroes usados pelos scripts:

- `MONGO_URI`: `mongodb://admin:admin123@localhost:27017`
- `MONGO_DB`: `amazonas_ecommerce`

Exemplo no PowerShell:

```powershell
$env:MONGO_URI = "mongodb://admin:admin123@localhost:27017"
$env:MONGO_DB = "amazonas_ecommerce"
python query_all_data.py
```

## Problemas comuns

### Erro ao subir com Docker

Se aparecer erro parecido com:

`open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`

Significa que o Docker Desktop nao esta ativo.

Passos:

1. Abra o Docker Desktop.
2. Aguarde o engine iniciar.
3. Rode novamente:

```powershell
docker compose up -d --build
```

### Recriar banco do zero

Se quiser executar novamente a inicializacao do `mongo-init/init.js` (limpar dados e recriar estrutura):

```powershell
docker compose down -v
docker compose up -d --build
```

## Comandos uteis

Parar ambiente:

```powershell
docker compose down
```

Ver logs do MongoDB:

```powershell
docker logs amazonas-mongodb
```

## Observacoes

- O script `mongo-init/init.js` roda apenas na primeira inicializacao do volume.
- O indice TTL da colecao `carrinho` remove documentos apos 48h (`172800` segundos).
