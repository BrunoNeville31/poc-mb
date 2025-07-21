from web3 import Web3
from utils.settings import settings


class MetaMaskService:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(settings.infura_url))
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to the Ethereum network")

    def get_balance(self, address: str) -> float:
        balance_wei = self.web3.eth.get_balance(address)
        return self.web3.from_wei(balance_wei, 'ether')

    def create_account(self) -> str:
        account = self.web3.eth.account.create()
        return account

    def send_transaction(self, from_address: str, to_address: str, amount: float, private_key: str):
        nonce = self.web3.eth.get_transaction_count(from_address)
        value = self.web3.to_wei(amount, 'ether')

        gas = self.web3.eth.estimate_gas({
            'to': to_address,
            'from': from_address,
            'value': value
        })       
        
        if gas is None:
            raise ValueError("Gas estimation failed")
        
        gas_price = self.web3.eth.gas_price
        
        if gas_price is None:
            raise ValueError("Gas price estimation failed")

        transaction = {
            'to': to_address,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce
        }

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return txn_hash.hex(), gas

