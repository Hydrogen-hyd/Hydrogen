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

@app.route('/connect_wallet', methods=['POST'])
def connect_wallet():
    data = request.get_json()
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'No address provided'}), 400

    # Add the wallet to our blockchain if it doesn't exist
    if address not in blockchain.wallets:
        blockchain.wallets[address] = {'balance': 0.0}  # Initial balance for new wallets
        blockchain.reputation_scores[address] = 50  # Initial reputation score
        blockchain.add_event('Wallet Connected', {'address': address})
        print(f"✅ New wallet connected: {address}")
    
    return jsonify({'success': True, 'address': address})

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
    blockchain.add_event('Faucet Used', {'wallet': wallet, 'amount': 10})  # Explicitly log the faucet event
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

@app.route('/hyd_price')
def hyd_price():
    price = blockchain.get_hyd_price()
    return render_template('hyd_price.html', price=price)

@app.route('/hyd_price_data')
def hyd_price_data():
    price = blockchain.get_hyd_price()
    return jsonify({'price': price})

if __name__ == '__main__':
    app.run(debug=True)
