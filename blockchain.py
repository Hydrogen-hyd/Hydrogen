import hashlib
import time
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.wallets = {}
        self.smart_contracts = []
        self.token_supply = 1000000  # Initial token supply (example 1,000,000 HYD)
        self.create_block(prev_hash="1", proof=100)
        self.events = []

    def create_wallet(self):
        address = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.wallets[address] = {'balance': 100.0}
        self.add_event('Wallet Created', {'address': address})
        return address

    def new_transaction(self, sender, receiver, amount):
        if sender not in self.wallets or receiver not in self.wallets:
            return "Sender or receiver wallet does not exist."
        
        if self.wallets[sender]['balance'] < amount + 0.5:
            return "Insufficient funds."
        
        fee = 0.5
        self.wallets[sender]['balance'] -= (amount + fee)
        self.wallets[receiver]['balance'] += amount

        transaction_data = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'fee': fee,
            'sender_balance': self.wallets[sender]['balance'],
            'receiver_balance': self.wallets[receiver]['balance'],
            'block_hash': self.chain[-1]['hash'],
            'prev_block_hash': self.chain[-2]['hash'] if len(self.chain) > 1 else 'None'
        }

        self.current_transactions.append(transaction_data)
        self.add_event('Transaction', transaction_data)
        return True

    def create_block(self, proof, prev_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev_hash,
        }
        block['hash'] = self.hash(block)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_event(self, event_type, event_data):
        timestamp = time.time()
        event = {
            'event': event_type,
            'timestamp': timestamp,
            'details': event_data
        }
        self.events.insert(0, event)

    def get_history(self):
        return self.events

    def create_smart_contract(self, contract_code):
        contract_hash = hashlib.sha256(contract_code.encode()).hexdigest()
        contract = {
            'contract_hash': contract_hash,
            'contract_code': contract_code,
            'timestamp': time.time(),
        }
        self.smart_contracts.append(contract)
        self.add_event('Smart Contract Created', {'contract_hash': contract_hash})
        return contract

    def execute_smart_contract(self, contract_hash):
        for contract in self.smart_contracts:
            if contract['contract_hash'] == contract_hash:
                self.add_event('Smart Contract Executed', {'contract_hash': contract_hash})
                return contract['contract_code']
        return "Smart contract not found."
        
    def mint_tokens(self, amount):
        self.token_supply += amount
        self.add_event('Tokens Minted', {'amount': amount, 'total_supply': self.token_supply})
        return True

    def burn_tokens(self, amount):
        if self.token_supply >= amount:
            self.token_supply -= amount
            self.add_event('Tokens Burned', {'amount': amount, 'total_supply': self.token_supply})
            return True
        return "Insufficient token supply to burn."

    def get_token_supply(self):
        return self.token_supply

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
