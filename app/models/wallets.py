from utils.mongo import Mongo

class Wallet(Mongo):
    def __init__(self):
        super().__init__("wallets")
    