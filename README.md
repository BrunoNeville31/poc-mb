## Objetivo do Projeto

- Criar carteiras na rede Etherium
- Realizar transações entre carteiras
- Visualizar históricos


## Planejamento da demanda

---

- Criação de Endpoints:
  - /wallets (POST e GET)
  - /wallet/:id (PATCH e GET)
  - /transactions
  - /transaction/validate (POST)
---

- Criar Models
  - wallets
  - accounts
  - account_versions

> O objetivo de account é saber o saldo que o ativo possui, e _versions é o hitorico da conta

---

- Criação dos Services Principais
  - Wallet MetaMask
  - Cache ou Async(Celery)


## Iniciando o projeto

```shell
# com uso do docker
cp .env.development .env
docker-compose build
docker-compose up -d

# manualmente
pip install -r requirements.txt
fastapi dev app/main.py
```

## Visualizando logs

```shell
docker-compose logs -f
```