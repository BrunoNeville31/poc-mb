from models.wallets import Wallet

class GetAllWallets:
    def __init__(self):
        self.wallet_model = Wallet()

    def execute(self):
        return self.wallet_model.find()