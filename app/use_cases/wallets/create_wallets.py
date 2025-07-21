from models.wallets import Wallet
from datetime import datetime

class CreateWallet:
    def __init__(self):
        self.wallet_model = Wallet()

    def execute(self, quantity):
        wallets = []
        timestamp = datetime.now()
        
        for i in range(quantity):
            wallet_data = {
                "id": timestamp.strftime("%Y%m%d%H%M%S") + str(i),
                "name": f"Wallet {i}",
                "balance": i * 100.0
            }
            self.wallet_model.insert_one(wallet_data)
            wallets.append(wallet_data)
        
        return wallets
