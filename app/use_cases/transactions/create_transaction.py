from datetime import datetime
from models.transactions import Transaction
from models.wallets import Wallet

from services.metamask import MetaMaskService

class CreateTransaction:
    def __init__(self):
        self.transaction_model = Transaction()
        self.wallet_model = Wallet()
        self.metamask_service = MetaMaskService()

    def execute(
      self, 
      from_wallet_id: str,
      to_wallet_id: str, 
      amount: float
    ):
        from_wallet = self.wallet_model.find_one({"address": from_wallet_id})
        to_wallet = self.wallet_model.find_one({"address": to_wallet_id})

        if not from_wallet:
            return {"error": "From wallet not found"}, 404
        if not to_wallet:
            return {"error": "To wallet not found"}, 404

        if from_wallet['balance'] < amount:
            return {"error": "Insufficient balance"}, 400

        tx_hash, gas = self.metamask_service.send_transaction(
            from_address=from_wallet['address'],
            to_address=to_wallet['address'],
            amount=amount,
            private_key=from_wallet['private_key']
        )

        transaction = {
            "from_wallet_id": from_wallet_id,
            "to_wallet_id": to_wallet_id,
            "amount": amount,
            "gas": gas,
            "tx_hash": tx_hash,
            "created_at": datetime.now()
        }
        self.transaction_model.insert_one(transaction)

        self.update_wallet_balances(from_wallet_id, to_wallet_id)

        return transaction

    def update_wallet_balances(self, from_wallet_id: str, to_wallet_id: str):
        balance_from  = self.metamask_service.get_balance(from_wallet_id)
        balance_to = self.metamask_service.get_balance(to_wallet_id)

        if not balance_from:
          return {"error": "From wallet not found"}, 404
        if not balance_to:
          return {"error": "To wallet not found"}, 404

        self.wallet_model.update_one({"address": from_wallet_id}, {"$set": {"balance": float(balance_from)}})
        self.wallet_model.update_one({"address": to_wallet_id}, {"$set": {"balance": float(balance_to)}})
        return True
