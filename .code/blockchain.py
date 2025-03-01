import hashlib
import time
import json
import random

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.wallets = {}
        self.smart_contracts = []
        self.token_supply = 1000000
        self.reputation_scores = {}
        self.create_block(prev_hash="1", proof=100)
        self.events = []
        self.network_info = {
            'chainId': '0x1337',
            'networkName': 'Hydrogen Blockchain',
            'symbol': 'HYD',
            'decimals': 18,
            'blockTime': 15  # 15 seconds block time
        }

    def get_network_info(self):
        return self.network_info

    def new_transaction(self, sender, receiver, amount, lock_time=None, private=False):
        if sender not in self.wallets and sender != "faucet":
            print(f"❌ Sender {sender} does not exist!")
            return "Sender does not exist."
        if receiver not in self.wallets:
            print(f"❌ Recipient {receiver} does not exist!")
            return "Recipient does not exist."
        if sender != "faucet" and self.wallets[sender]['balance'] < amount + 0.5:
            print(f"❌ Insufficient funds for {sender}")
            return "Insufficient funds."

        # Add nonce to transaction for MetaMask compatibility
        nonce = len([tx for tx in self.current_transactions if tx['sender'] == sender])
        
        fee = 0.5
        if sender != "faucet":
            self.wallets[sender]['balance'] -= (amount + fee)
        self.wallets[receiver]['balance'] += amount

        transaction_data = {
            'sender': sender if not private else "Anonymous",
            'receiver': receiver if not private else "Anonymous",
            'amount': amount if not private else "Hidden",
            'fee': fee,
            'nonce': nonce,
            'block_hash': self.chain[-1]['hash'],
            'prev_block_hash': self.chain[-2]['hash'] if len(self.chain) > 1 else 'None',
            'lock_time': lock_time
        }

        self.current_transactions.append(transaction_data)
        self.add_event('Transaction', transaction_data)
        self.update_reputation(sender, receiver)

        return transaction_data

    def faucet(self, address):
        if address in self.wallets:
            self.wallets[address]['balance'] += 10
            self.add_event('Faucet Claim', {'address': address, 'amount': 10})

    def update_reputation(self, sender, receiver):
        if sender in self.reputation_scores:
            self.reputation_scores[sender] = max(0, self.reputation_scores[sender] - random.randint(1, 5))
        if receiver in self.reputation_scores:
            self.reputation_scores[receiver] = min(100, self.reputation_scores[receiver] + random.randint(1, 5))

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

    def get_wallets(self):
        return self.wallets

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
        self.smart_contracts.append({'contract_hash': contract_hash, 'contract_code': contract_code})
        self.add_event('Smart Contract Created', {'contract_hash': contract_hash})

    def execute_smart_contract(self, contract_hash):
        for contract in self.smart_contracts:
            if contract['contract_hash'] == contract_hash:
                self.add_event('Smart Contract Executed', {'contract_hash': contract_hash})
                return "Smart contract executed successfully."
        return "Contract not found."

    def get_smart_contracts(self):
        return self.smart_contracts

    def add_event(self, event, details):
        self.events.append({
            'event': event,
            'details': details,
            'timestamp': time.time()
        })

    def get_history(self):
        return self.events

    def get_reputation_scores(self):
        return self.reputation_scores
