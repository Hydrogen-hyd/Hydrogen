from flask import Flask, request, jsonify, render_template, redirect, url_for
import time
import hashlib
import json
import random
from datetime import datetime
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

# Custom Jinja2 filter for formatting timestamps
@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return render_template(
        'index.html',
        wallets=blockchain.get_wallets(),
        smart_contracts=blockchain.get_smart_contracts(),
        token_supply=blockchain.get_token_supply(),
        reputation_scores=blockchain.get_reputation_scores()
    )

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    wallet_address = blockchain.create_wallet()
    if wallet_address:
        print(f"✅ New wallet created: {wallet_address}")  # Debugging log
    else:
        print("❌ Wallet creation failed!")  # Debugging log
    return redirect(url_for('index'))

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    sender = request.form['sender']
    receiver = request.form['recipient']
    amount = float(request.form['amount'])
    private = request.form.get('private_tx_enabled') == 'on'

    lock_time = None
    if 'lock_time_enabled' in request.form:
        lock_time = request.form.get('lock_time')
        if lock_time:
            lock_time = datetime.strptime(lock_time, '%Y-%m-%dT%H:%M').timestamp()

    blockchain.new_transaction(sender, receiver, amount, lock_time, private)
    return redirect(url_for('index'))

@app.route('/faucet', methods=['POST'])
def faucet():
    wallet = request.form['wallet']
    blockchain.faucet(wallet)
    return redirect(url_for('index'))

@app.route('/mint_tokens', methods=['POST'])
def mint_tokens():
    amount = int(request.form['mint_amount'])
    blockchain.mint_tokens(amount)
    return redirect(url_for('index'))

@app.route('/burn_tokens', methods=['POST'])
def burn_tokens():
    amount = int(request.form['burn_amount'])
    blockchain.burn_tokens(amount)
    return redirect(url_for('index'))

@app.route('/create_smart_contract', methods=['POST'])
def create_smart_contract():
    contract_code = request.form['contract_code']
    blockchain.create_smart_contract(contract_code)
    return redirect(url_for('index'))

@app.route('/execute_smart_contract', methods=['POST'])
def execute_smart_contract():
    contract_hash = request.form['contract_hash']
    blockchain.execute_smart_contract(contract_hash)
    return redirect(url_for('index'))

@app.route('/analytics')
def analytics():
    history = blockchain.get_history()
    total_blocks = len(blockchain.chain)
    total_transactions = sum(len(block['transactions']) for block in blockchain.chain)
    total_wallets = len(blockchain.wallets)
    token_supply = blockchain.token_supply
    circulating_supply = sum(wallet['balance'] for wallet in blockchain.wallets.values())

    return render_template(
        'analytics.html',
        history=history,
        total_blocks=total_blocks,
        total_transactions=total_transactions,
        total_wallets=total_wallets,
        token_supply=token_supply,
        circulating_supply=circulating_supply
    )

if __name__ == '__main__':
    app.run(debug=True)
