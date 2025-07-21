
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from use_cases.wallets.get_all_wallets import GetAllWallets
from use_cases.wallets.get_one_wallet_by_id import GetOneWalletById
from use_cases.wallets.create_wallets import CreateWallet

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
    get_all_wallets = GetAllWallets()
    wallets = get_all_wallets.execute()
    if not wallets:
        return []
    
    return [Wallet(**wallet) for wallet in wallets]

@app.get(
  "/wallets/{wallet_id}",
  summary="Obter detalhes da wallet",
  tags=["Wallets"],
  response_model=Wallet
)
async def get_wallet(wallet_id: str):
    get_one_wallet = GetOneWalletById()
    wallet = get_one_wallet.execute(id=wallet_id)
    
    if not wallet:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Wallet(**wallet)


class CreateWalletRequest(BaseModel):
    quantity: int

@app.post(
  "/wallets",
  summary="Criar nova wallet",
  tags=["Wallets"],
  response_model=list[Wallet]
)
async def create_wallet(wallet: CreateWalletRequest):
    create_wallet_use_case = CreateWallet()

    create_wallet_data = create_wallet_use_case.execute(wallet.quantity)

    if not create_wallet_data:
        return {"error": "Failed to create wallets"}
    
    return [Wallet(**data) for data in create_wallet_data]

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