from models.transactions import Transaction

class GetAllTransactions:
    def __init__(self):
        self.transaction_model = Transaction()

    def execute(self):
        return self.transaction_model.find({})