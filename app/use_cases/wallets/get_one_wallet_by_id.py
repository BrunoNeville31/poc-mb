from models.wallets import Wallet

class GetOneWalletById:
    def __init__(self):
        self.wallet_model = Wallet()

    def execute(self, id=None):
        data = self.wallet_model.find_one({"id": id})

        if not data:
            return None
        return data