from flask import Flask, request, jsonify, render_template, redirect, url_for
import time
import hashlib
import json
import random
from datetime import datetime

app = Flask(__name__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.wallets = {}
        self.smart_contracts = []
        self.token_supply = 1000000  # Initial supply
        self.reputation_scores = {}  # Store reputation scores
        self.create_block(prev_hash="1", proof=100)
        self.events = []

    def create_wallet(self):
        address = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.wallets[address] = {'balance': 100.0}
        self.reputation_scores[address] = 50  # Neutral reputation
        self.add_event('Wallet Created', {'address': address})
        return address

    def new_transaction(self, sender, receiver, amount, lock_time=None, private=False):
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
            'sender': sender if not private else "Anonymous",
            'receiver': receiver if not private else "Anonymous",
            'amount': amount if not private else "Hidden",
            'fee': fee,
            'block_hash': self.chain[-1]['hash'],
            'prev_block_hash': self.chain[-2]['hash'] if len(self.chain) > 1 else 'None',
            'lock_time': lock_time
        }

        self.current_transactions.append(transaction_data)
        self.add_event('Transaction', transaction_data)
        
        self.update_reputation(sender, receiver)

        return transaction_data

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

    def get_reputation(self, address):
        return self.reputation_scores.get(address, 0)

    def add_event(self, event, details):
        self.events.append({
            'event': event,
            'details': details,
            'timestamp': time.time()
        })

blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain)

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    address = blockchain.create_wallet()
    return redirect(url_for('index'))

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    sender = request.form['sender']
    receiver = request.form['recipient']
    amount = float(request.form['amount'])
    private = request.form.get('private') == 'on'

    lock_time_enabled = request.form.get('lock_time_enabled')
    lock_time = None
    if lock_time_enabled:
        lock_time = request.form.get('lock_time')
        if lock_time:
            lock_time = datetime.strptime(lock_time, '%Y-%m-%dT%H:%M').timestamp()

    blockchain.new_transaction(sender, receiver, amount, lock_time, private)
    return redirect(url_for('index'))

@app.route('/get_reputation/<address>')
def get_reputation(address):
    score = blockchain.get_reputation(address)
    return jsonify({'address': address, 'reputation': score})

if __name__ == '__main__':
    app.run(debug=True)
