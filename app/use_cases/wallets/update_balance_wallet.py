from models.wallets import Wallet
from datetime import datetime

from services.metamask import MetaMaskService

class UpdateBalanceWallet:
	def __init__(self):
		self.wallet_model = Wallet()
		self.metamask_service = MetaMaskService()

	def execute(self, wallet_id):
		data = self.wallet_model.find_one({"id": wallet_id})
		balance = self.metamask_service.get_balance(data["address"])

		if not data:
			return {"error": "Wallet not found"}, 404
		if data["balance"] == balance:
			return {"message": "Balance is already up to date"}, 200
		
		data["balance"] = float(balance)
		self.wallet_model.update_one({"id": wallet_id}, {"$set": {"balance": float(balance)}})

		return data
