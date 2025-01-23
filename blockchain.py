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

    def new_transaction(self, sender, receiver, amount, lock_time=None):
        if sender not in self.wallets and sender != "faucet":
            return "Sender does not exist."
        if receiver not in self.wallets:
            return "Recipient does not exist."
        if sender != "faucet" and self.wallets[sender]['balance'] < amount + 0.5:
            return "Insufficient funds."
        
        fee = 0.5
        if sender != "faucet":
            self.wallets[sender]['balance'] -= (amount + fee)
        self.wallets[receiver]['balance'] += amount

        transaction_data = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'fee': fee,
            'sender_balance': self.wallets.get(sender, {}).get('balance', 0),
            'receiver_balance': self.wallets[receiver]['balance'],
            'block_hash': self.chain[-1]['hash'],
            'prev_block_hash': self.chain[-2]['hash'] if len(self.chain) > 1 else 'None',
            'lock_time': lock_time
        }

        self.current_transactions.append(transaction_data)
        self.add_event('Transaction', transaction_data)
        return transaction_data

    def create_block(self, proof, prev_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev_hash,
            'hash': hashlib.sha256(json.dumps(self.current_transactions).encode()).hexdigest()
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def get_token_supply(self):
        return self.token_supply

    def mint_tokens(self, amount):
        self.token_supply += amount
        self.add_event('Tokens Minted', {'amount': amount})

    def burn_tokens(self, amount):
        if self.token_supply < amount:
            return "Insufficient token supply to burn."
        self.token_supply -= amount
        self.add_event('Tokens Burned', {'amount': amount})

    def create_smart_contract(self, contract_code):
        contract_hash = hashlib.sha256(contract_code.encode()).hexdigest()
        self.smart_contracts.append({'contract_code': contract_code, 'contract_hash': contract_hash})
        self.add_event('Smart Contract Created', {'contract_hash': contract_hash})
        return {'contract_code': contract_code, 'contract_hash': contract_hash}

    def execute_smart_contract(self, contract_hash):
        contract = next((contract for contract in self.smart_contracts if contract['contract_hash'] == contract_hash), None)
        if contract:
            self.add_event('Smart Contract Executed', {'contract_hash': contract_hash})
            return {'status': 'Executed', 'contract_hash': contract_hash}
        return {'status': 'Contract Not Found'}

    def add_event(self, event, details):
        self.events.append({
            'event': event,
            'details': details,
            'timestamp': time.time()
        })

    def get_history(self):
        return self.events
