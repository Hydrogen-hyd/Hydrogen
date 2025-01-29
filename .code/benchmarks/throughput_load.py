import time
import threading
import sys
import os

# Ensure the parent directory is accessible for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blockchain import Blockchain  # Import Blockchain from the main project

def process_transactions(blockchain, num_transactions, batch_size=1000):
    """
    Processes a large number of transactions in batches to simulate real-world load.
    
    Args:
        blockchain (Blockchain): An instance of the blockchain.
        num_transactions (int): Total number of transactions to process.
        batch_size (int): Number of transactions before creating a block.
    
    Returns:
        float: Transactions processed per second under load.
    """
    sender = blockchain.create_wallet()
    receiver = blockchain.create_wallet()
    
    # Ensure sender has enough balance
    blockchain.wallets[sender]['balance'] = 1e9
    
    start_time = time.time()
    
    for i in range(num_transactions):
        blockchain.new_transaction(sender, receiver, amount=1)
        
        # Periodically create a block to simulate a real blockchain
        if len(blockchain.current_transactions) >= batch_size:
            blockchain.create_block(proof=100, prev_hash=blockchain.chain[-1]['hash'])
    
    # Create a final block for remaining transactions
    if blockchain.current_transactions:
        blockchain.create_block(proof=100, prev_hash=blockchain.chain[-1]['hash'])
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    tps = num_transactions / elapsed_time
    
    return tps

def benchmark_throughput(blockchain, num_transactions=10000, batch_size=1000, num_threads=4):
    """
    Runs a throughput benchmark by processing transactions in multiple threads.
    
    Args:
        blockchain (Blockchain): An instance of the blockchain.
        num_transactions (int): Total transactions to process.
        batch_size (int): Transactions per block.
        num_threads (int): Number of concurrent threads.
    
    Returns:
        float: Overall transactions per second (TPS).
    """
    threads = []
    transactions_per_thread = num_transactions // num_threads
    
    start_time = time.time()
    
    for _ in range(num_threads):
        thread = threading.Thread(target=process_transactions, args=(blockchain, transactions_per_thread, batch_size))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    tps = num_transactions / elapsed_time
    
    return tps

if __name__ == "__main__":
    # Initialize blockchain
    blockchain = Blockchain()
    
    # Configurable parameters
    NUM_TRANSACTIONS = 20000  # Adjust load size
    BATCH_SIZE = 1000         # Transactions per block
    NUM_THREADS = 4           # Number of concurrent workers

    print(f"Running throughput benchmark with {NUM_TRANSACTIONS} transactions, batch size: {BATCH_SIZE}, using {NUM_THREADS} threads...")

    tps = benchmark_throughput(blockchain, NUM_TRANSACTIONS, BATCH_SIZE, NUM_THREADS)

    print(f"Processed {NUM_TRANSACTIONS} transactions under load.")
    print(f"Throughput (TPS under load): {tps:.2f}")
