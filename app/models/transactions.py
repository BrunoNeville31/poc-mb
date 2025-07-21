from utils.mongo import Mongo

class Transaction(Mongo):
    def __init__(self):
        super().__init__("transactions")

class TransactionVersion(Mongo):
    def __init__(self):
        super().__init__("transaction_versions")