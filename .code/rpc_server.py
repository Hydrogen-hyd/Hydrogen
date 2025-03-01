from flask import Flask, request, jsonify
from flask_cors import CORS
from blockchain import Blockchain
import json
import hashlib
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
blockchain = Blockchain()

def handle_eth_request(method, params):
    if method == 'eth_chainId':
        return blockchain.network_info['chainId']
    
    elif method == 'eth_getBalance':
        address = params[0]
        if address in blockchain.wallets:
            # Convert balance to Wei (18 decimals)
            balance_wei = int(blockchain.wallets[address]['balance'] * 10**18)
            return hex(balance_wei)
        return hex(0)
    
    elif method == 'eth_accounts':
        return list(blockchain.wallets.keys())
    
    elif method == 'eth_blockNumber':
        return hex(len(blockchain.chain))
    
    elif method == 'eth_getBlockByNumber':
        block_num = int(params[0], 16) if params[0] != 'latest' else len(blockchain.chain) - 1
        if 0 <= block_num < len(blockchain.chain):
            block = blockchain.chain[block_num]
            return {
                'number': hex(block['index']),
                'hash': block['hash'],
                'parentHash': block['prev_hash'],
                'timestamp': hex(int(block['timestamp'])),
                'transactions': [tx['hash'] for tx in block['transactions']] if block['transactions'] else []
            }
        return None
    
    elif method == 'eth_sendTransaction':
        tx = params[0]
        from_addr = tx['from']
        to_addr = tx['to']
        value = int(tx['value'], 16) / 10**18  # Convert from Wei to HYD
        
        result = blockchain.new_transaction(from_addr, to_addr, value)
        if isinstance(result, str) and 'error' in result.lower():
            return {'error': result}
            
        # Create a transaction hash
        tx_hash = hashlib.sha256(json.dumps(result).encode()).hexdigest()
        return '0x' + tx_hash
    
    elif method == 'eth_getTransactionCount':
        address = params[0]
        # Count number of transactions from this address
        nonce = len([tx for block in blockchain.chain 
                    for tx in block['transactions'] 
                    if tx.get('sender') == address])
        return hex(nonce)
    
    return None

@app.route('/', methods=['POST'])
def handle_request():
    try:
        data = request.get_json()
        
        # Handle batch requests
        if isinstance(data, list):
            responses = []
            for req in data:
                method = req.get('method')
                params = req.get('params', [])
                result = handle_eth_request(method, params)
                responses.append({
                    'jsonrpc': '2.0',
                    'id': req.get('id'),
                    'result': result
                })
            return jsonify(responses)
        
        # Handle single request
        method = data.get('method')
        params = data.get('params', [])
        result = handle_eth_request(method, params)
        
        response = {
            'jsonrpc': '2.0',
            'id': data.get('id'),
            'result': result
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'id': data.get('id'),
            'error': {'code': -32603, 'message': str(e)}
        })

if __name__ == '__main__':
    # Run on port 8545 which is the default for Ethereum RPC
    app.run(host='0.0.0.0', port=8545) 
