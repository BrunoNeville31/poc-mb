from models.transactions import Transaction

class GetTransactionsByWallet:
    def __init__(self):
        self.transaction_model = Transaction()

    def execute(self, address: str):
        return self.transaction_model.find({
            "$or": [
            {"from_wallet_id": address},
            {"to_wallet_id": address}
            ]
        })