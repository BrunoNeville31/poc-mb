from models.transactions import Transaction

class GetOneTransactionById:
    def __init__(self):
        self.transaction_model = Transaction()

    def execute(self, transaction_id: str):
        return self.transaction_model.find_one({"id": transaction_id})