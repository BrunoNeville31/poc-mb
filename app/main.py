
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
# Health check
"""
@app.get(
  "/health_check", 
  summary="Verificar estado da aplicação",
  tags=["Health Check"]
)
async def health_check():
    return {
      "message": "Aplicação ETH POC em execução!",
      "status": "ok"
    }


"""
# Wallets endpoint
"""

class Wallet(BaseModel):
    id: str
    name: str
    balance: float

@app.get(
  "/wallets",
  summary="Listar wallets",
  tags=["Wallets"],
  response_model=list[Wallet]
)
async def get_wallets():
    return [
        Wallet(id="1", name="Wallet 1", balance=100.0),
        Wallet(id="2", name="Wallet 2", balance=200.0)
    ]

@app.get(
  "/wallets/{wallet_id}",
  summary="Obter detalhes da wallet",
  tags=["Wallets"],
  response_model=Wallet
)
async def get_wallet(wallet_id: str):
    return Wallet(id=wallet_id, name=f"Wallet {wallet_id}", balance=100.0)


class CreateWalletRequest(BaseModel):
    quantity: int

@app.post(
  "/wallets",
  summary="Criar nova wallet",
  tags=["Wallets"],
  response_model=Wallet
)
async def create_wallet(wallet: CreateWalletRequest):
    return Wallet(id="3", name=f"Wallet {wallet.quantity}", balance=wallet.quantity * 100.0)


"""
# Transactions endpoint
"""

class Transaction(BaseModel):
    id: str
    wallet_id: str
    amount: float

@app.get(
  "/transactions",
  summary="Listar transações",
  tags=["Transactions"],
  response_model=list[Transaction]
)
async def get_transactions():
    return [
        Transaction(id="1", wallet_id="1", amount=50.0),
        Transaction(id="2", wallet_id="2", amount=75.0)
    ]

@app.get(
  "/transactions/{transaction_id}",
  summary="Obter detalhes da transação",
  tags=["Transactions"],
  response_model=Transaction
)
async def get_transaction(transaction_id: str):
    return Transaction(id=transaction_id, wallet_id="1", amount=50.0)

class CreateTransactionRequest(BaseModel):
    wallet_id: str
    amount: float

@app.post(
  "/transactions",
  summary="Criar nova transação",
  tags=["Transactions"],
  response_model=Transaction
)
async def create_transaction(transaction: CreateTransactionRequest):
    return Transaction(id="3", wallet_id=transaction.wallet_id, amount=transaction.amount)