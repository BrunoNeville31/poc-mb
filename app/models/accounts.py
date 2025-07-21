from utils.mongo import Mongo

class Account(Mongo):
    def __init__(self):
        super().__init__("accounts")
