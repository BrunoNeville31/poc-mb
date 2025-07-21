
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from use_cases.wallets.get_all_wallets import GetAllWallets
from use_cases.wallets.get_one_wallet_by_id import GetOneWalletById
from use_cases.wallets.create_wallets import CreateWallet
from use_cases.wallets.update_balance_wallet import UpdateBalanceWallet

from use_cases.transactions.get_one_transaction_by_id import GetOneTransactionById
from use_cases.transactions.get_all_transactions import GetAllTransactions
from use_cases.transactions.create_transaction import CreateTransaction
from use_cases.transactions.get_transactions_by_wallet import GetTransactionsByWallet

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
    address: str
    created_at: datetime


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
        return Response(
          status_code=status.HTTP_400_BAD_REQUEST, 
          content={"message": "Erro ao criar wallets"}
        )

    return [Wallet(**data) for data in create_wallet_data]


@app.patch(
  "/wallets/{wallet_id}/update_balance",
  summary="Atualizar saldo da wallet",
  tags=["Wallets"],
  response_model=Wallet
)
async def update_wallet_balance(wallet_id: str):
    update_balance_wallet = UpdateBalanceWallet()
    wallet = update_balance_wallet.execute(wallet_id=wallet_id)

    if not wallet:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Wallet(**wallet)

"""
# Transactions endpoint
"""

class Transaction(BaseModel):
    from_wallet_id: str
    to_wallet_id: str
    amount: float
    gas: float
    tx_hash: str
    created_at: datetime

@app.get(
  "/transactions",
  summary="Listar transações",
  tags=["Transactions"],
  response_model=list[Transaction]
)
async def get_transactions():
    get_all_transactions = GetAllTransactions()
    transactions = get_all_transactions.execute()
    if not transactions:
        return []
    return [Transaction(**tx) for tx in transactions]


@app.get(
  "/transactions/{transaction_id}",
  summary="Obter detalhes da transação",
  tags=["Transactions"],
  response_model=Transaction
)
async def get_transaction(transaction_id: str):
    get_one_transaction = GetOneTransactionById()
    transaction = get_one_transaction.execute(transaction_id=transaction_id)

    if not transaction:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Transaction(**transaction)

class CreateTransactionRequest(BaseModel):
    wallet_from: str
    wallet_to: str
    amount: float

@app.post(
  "/transactions",
  summary="Criar nova transação",
  tags=["Transactions"],
  response_model=Transaction
)
async def create_transaction(transaction: CreateTransactionRequest):
    create_transaction_use_case = CreateTransaction()
    transaction_data = create_transaction_use_case.execute(
        from_wallet_id=transaction.wallet_from,
        to_wallet_id=transaction.wallet_to,
        amount=transaction.amount
    )
    if not transaction_data:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"message": "Erro ao criar transação"}  
        )
    return Transaction(**transaction_data)

@app.get(
  "/transactions/wallet/{address}",
  summary="Listar transações por endereço da wallet",
  tags=["Transactions"],
  response_model=list[Transaction]
)
async def get_transactions_by_wallet(address: str):
    get_transactions_by_wallet = GetTransactionsByWallet()
    transactions = get_transactions_by_wallet.execute(address=address)
    if not transactions:
        return []
    return [Transaction(**tx) for tx in transactions]