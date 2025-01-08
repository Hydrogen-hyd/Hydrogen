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
    return render_template('index.html', wallets=wallets, history=history)

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

if __name__ == '__main__':
    app.run(debug=True)
