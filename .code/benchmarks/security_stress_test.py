import time
import random
import sys
import os

# Ensure the parent directory is accessible for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blockchain import Blockchain  # Import Blockchain from the main project

def simulate_attack(blockchain, attack_type, num_attempts):
    """
    Simulates different types of security attacks.
    
    Args:
        blockchain (Blockchain): An instance of the blockchain.
        attack_type (str): Type of attack ('double_spend', 'spam', 'sybil').
        num_attempts (int): Number of attempts to test security.
    
    Returns:
        float: Time taken to detect/prevent the attack.
    """
    sender = blockchain.create_wallet()
    receiver = blockchain.create_wallet()
    
    # Ensure sender has enough balance
    blockchain.wallets[sender]['balance'] = 1e6
    
    start_time = time.time()
    
    if attack_type == "double_spend":
        for _ in range(num_attempts):
            blockchain.new_transaction(sender, receiver, amount=1)
            blockchain.new_transaction(sender, receiver, amount=1)  # Attempt to double-spend
        
    elif attack_type == "spam":
        for _ in range(num_attempts):
            blockchain.new_transaction(sender, receiver, amount=random.uniform(0.01, 10))
        
    elif attack_type == "sybil":
        for _ in range(num_attempts):
            blockchain.create_wallet()  # Flood the system with fake wallets
    
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    return elapsed_time

if __name__ == "__main__":
    blockchain = Blockchain()
    
    NUM_ATTEMPTS = 1000
    
    print("Running security stress test...\n")
    
    for attack in ["double_spend", "spam", "sybil"]:
        time_taken = simulate_attack(blockchain, attack, NUM_ATTEMPTS)
        print(f"{attack.capitalize()} Attack: {time_taken:.2f} seconds to execute {NUM_ATTEMPTS} attempts.")
    
    print("\nSecurity stress test completed.")
