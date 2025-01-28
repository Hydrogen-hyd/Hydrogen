import time
import random

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def create_genesis_block(self):
        block = {
            "index": 0,
            "timestamp": time.time(),
            "transactions": [],
            "previous_hash": "0",
            "nonce": 0,
        }
        self.chain.append(block)
        return block

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "transactions": transactions,
            "previous_hash": self.hash_block(previous_block),
            "nonce": self.proof_of_work(),
        }
        self.chain.append(block)
        return block

    def hash_block(self, block):
        block_string = f"{block['index']}{block['timestamp']}{block['transactions']}{block['previous_hash']}{block['nonce']}"
        return hash(block_string)

    def proof_of_work(self):
        nonce = 0
        while not self.is_valid_nonce(nonce):
            nonce += 1
        return nonce

    def is_valid_nonce(self, nonce):
        # Simple proof of work function (e.g., find nonce where hash ends in 0)
        return str(nonce).endswith("0")

def benchmark_block_time(blockchain, num_blocks=10, transactions_per_block=5):
    if not blockchain.chain:
        blockchain.create_genesis_block()

    total_time = 0
    inter_block_times = []
    prev_timestamp = blockchain.chain[-1]["timestamp"]

    for _ in range(num_blocks):
        transactions = [{"sender": f"user_{random.randint(1, 100)}", "receiver": f"user_{random.randint(1, 100)}", "amount": random.randint(1, 100)} for _ in range(transactions_per_block)]
        
        start_time = time.time()
        new_block = blockchain.add_block(transactions)
        end_time = time.time()

        block_time = end_time - start_time
        inter_block_time = new_block["timestamp"] - prev_timestamp
        prev_timestamp = new_block["timestamp"]

        total_time += block_time
        inter_block_times.append(inter_block_time)

        print(f"Block {new_block['index']} added: Block time = {block_time:.4f}s, Inter-block time = {inter_block_time:.4f}s")

    avg_block_time = total_time / num_blocks
    avg_inter_block_time = sum(inter_block_times) / len(inter_block_times)

    print("\nBenchmark Results:")
    print(f"Average block creation time: {avg_block_time:.4f}s")
    print(f"Average inter-block time: {avg_inter_block_time:.4f}s")

if __name__ == "__main__":
    blockchain = Blockchain()
    benchmark_block_time(blockchain)
