import time
import sys
from pathlib import Path

# Ensure the blockchain module is in the path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from blockchain import Blockchain  # Import Blockchain after adding the correct path

def benchmark_transactions(blockchain, num_transactions):
    """
    Benchmarks the transaction processing speed.
    Args:
        blockchain (Blockchain): An instance of the blockchain.
        num_transactions (int): Number of transactions to process.
    Returns:
        float: Transactions processed per second.
    """
    # Create wallets for the benchmark
    sender = blockchain.create_wallet()
    receiver = blockchain.create_wallet()

    # Ensure sender has enough balance
    blockchain.wallets[sender]['balance'] = 1e6

    # Start benchmarking
    start_time = time.time()

    for _ in range(num_transactions):
        blockchain.new_transaction(sender, receiver, amount=1)

        # Optionally create a block after every N transactions (e.g., every 1000 transactions)
        if len(blockchain.current_transactions) >= 1000:
            blockchain.create_block(proof=100, prev_hash=blockchain.chain[-1]['hash'])

    # Final block creation to include remaining transactions
    if blockchain.current_transactions:
        blockchain.create_block(proof=100, prev_hash=blockchain.chain[-1]['hash'])

    end_time = time.time()

    elapsed_time = end_time - start_time
    tps = num_transactions / elapsed_time

    return tps

if __name__ == "__main__":
    # Initialize the blockchain
    blockchain = Blockchain()

    # Number of transactions to test
    NUM_TRANSACTIONS = 10000  # Adjust as needed

    # Run the benchmark
    tps = benchmark_transactions(blockchain, NUM_TRANSACTIONS)

    print(f"Processed {NUM_TRANSACTIONS} transactions.")
    print(f"Transactions per second (TPS): {tps:.2f}")
