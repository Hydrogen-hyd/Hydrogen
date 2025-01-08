import hashlib
import time
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.wallets = {}
        self.create_block(prev_hash="1", proof=100)
        self.events = []  # To store event history

    def create_wallet(self):
        address = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.wallets[address] = {'balance': 100.0}  # Initial balance of 100.0 HYD
        self.add_event('Wallet Created', {'address': address})
        return address

    def new_transaction(self, sender, receiver, amount):
        if sender not in self.wallets or receiver not in self.wallets:
            return "Sender or receiver wallet does not exist."
        
        if self.wallets[sender]['balance'] < amount + 0.5:  # 0.5 is the fee
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
        self.events.insert(0, event)  # Insert at the top to ensure latest event is first

    def get_history(self):
        return self.events
