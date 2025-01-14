from flask import Flask, jsonify, request, render_template, redirect, url_for
from blockchain import Blockchain
from datetime import datetime

app = Flask(__name__)

blockchain = Blockchain()

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    wallets = blockchain.wallets
    smart_contracts = blockchain.smart_contracts
    token_supply = blockchain.get_token_supply()
    return render_template('index.html', wallets=wallets, smart_contracts=smart_contracts, token_supply=token_supply)

@app.route('/analytics')
def analytics():
    history = blockchain.get_history()
    token_supply = blockchain.get_token_supply()
    total_blocks = len(blockchain.chain)
    
    # Fix for total transactions
    total_transactions = sum(len(block.get('transactions', [])) for block in blockchain.chain)
    
    total_wallets = len(blockchain.wallets)
    circulating_supply = sum(wallet['balance'] for wallet in blockchain.wallets.values())
    return render_template('analytics.html', 
                           history=history, 
                           token_supply=token_supply, 
                           total_blocks=total_blocks, 
                           total_transactions=total_transactions, 
                           total_wallets=total_wallets, 
                           circulating_supply=circulating_supply)

@app.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    if request.method == 'POST':
        address = blockchain.create_wallet()
        return redirect(url_for('index'))
    return render_template('create_wallet.html')

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    sender = request.form['sender']
    receiver = request.form['recipient']
    amount = float(request.form['amount'])
    blockchain.new_transaction(sender, receiver, amount)
    return redirect(url_for('index'))

@app.route('/create_smart_contract', methods=['POST'])
def create_smart_contract():
    contract_code = request.form['contract_code']
    contract = blockchain.create_smart_contract(contract_code)
    return redirect(url_for('index'))

@app.route('/execute_smart_contract', methods=['POST'])
def execute_smart_contract():
    contract_hash = request.form['contract_hash']
    result = blockchain.execute_smart_contract(contract_hash)
    return redirect(url_for('index'))

@app.route('/mint_tokens', methods=['POST'])
def mint_tokens():
    mint_amount = int(request.form['mint_amount'])
    blockchain.mint_tokens(mint_amount)
    return redirect(url_for('index'))

@app.route('/burn_tokens', methods=['POST'])
def burn_tokens():
    burn_amount = int(request.form['burn_amount'])
    blockchain.burn_tokens(burn_amount)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
