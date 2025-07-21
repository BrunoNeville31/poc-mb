from models.wallets import Wallet
from datetime import datetime

from services.metamask import MetaMaskService

class CreateWallet:
    def __init__(self):
        self.wallet_model = Wallet()
        self.metamask_service = MetaMaskService()

    def execute(self, quantity):
        wallets = []
        timestamp = datetime.now()
        
        for i in range(quantity):
            eth_created = self.metamask_service.create_account()
            balance = self.metamask_service.get_balance(eth_created.address)
            
            wallet_data = {
                "id": timestamp.strftime("%Y%m%d%H%M%S") + str(i),
                "address": eth_created.address,
                "private_key": eth_created.key.hex(),
                "created_at": datetime.now(),
                "name": f"Carteira {eth_created.address[:6]}**{eth_created.address[-6:]}",
                "balance": balance
            }
            self.wallet_model.insert_one(wallet_data)
            wallets.append(wallet_data)
        
        return wallets
