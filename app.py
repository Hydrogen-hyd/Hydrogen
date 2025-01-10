from flask import Flask, jsonify, request, render_template, redirect, url_for
from blockchain import Blockchain
from datetime import datetime

app = Flask(__name__)

# Initialize the blockchain
blockchain = Blockchain()

# Custom filter for date formatting
@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    """Homepage that displays wallets and events"""
    wallets = blockchain.wallets
    history = blockchain.get_history()  # Get full history (wallet creation + transactions)
    smart_contracts = blockchain.smart_contracts  # Get list of smart contracts
    return render_template('index.html', wallets=wallets, history=history, smart_contracts=smart_contracts)

@app.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    """Create a new wallet"""
    if request.method == 'POST':
        address = blockchain.create_wallet()
        return redirect(url_for('index'))
    return render_template('create_wallet.html')

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    """Send HYD tokens from one wallet to another"""
    sender = request.form['sender']
    receiver = request.form['recipient']
    amount = float(request.form['amount'])

    # Send the transaction
    blockchain.new_transaction(sender, receiver, amount)
    return redirect(url_for('index'))

@app.route('/create_smart_contract', methods=['POST'])
def create_smart_contract():
    """Create a new smart contract"""
    contract_code = request.form['contract_code']
    contract = blockchain.create_smart_contract(contract_code)
    return redirect(url_for('index'))

@app.route('/execute_smart_contract', methods=['POST'])
def execute_smart_contract():
    """Execute a smart contract"""
    contract_hash = request.form['contract_hash']
    result = blockchain.execute_smart_contract(contract_hash)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
