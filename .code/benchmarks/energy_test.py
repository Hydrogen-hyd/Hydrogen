import time
import sys
import os
import psutil  # External library for CPU and energy stats

# Ensure the parent directory is accessible for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blockchain import Blockchain

def measure_energy_usage(blockchain, num_blocks=10):
    """
    Measures energy consumption by tracking CPU usage while mining blocks.
    
    Args:
        blockchain (Blockchain): An instance of the blockchain.
        num_blocks (int): Number of blocks to mine.
    
    Returns:
        dict: CPU usage and estimated energy usage.
    """
    print(f"Measuring energy consumption for mining {num_blocks} blocks...")

    initial_cpu_usage = psutil.cpu_percent(interval=1)
    start_time = time.time()
    
    for _ in range(num_blocks):
        blockchain.create_block(proof=100, prev_hash=blockchain.chain[-1]['hash'])

    end_time = time.time()
    final_cpu_usage = psutil.cpu_percent(interval=1)

    elapsed_time = end_time - start_time
    avg_cpu_usage = (initial_cpu_usage + final_cpu_usage) / 2

    # Estimated energy consumption (simple model: CPU usage % * time)
    estimated_energy = avg_cpu_usage * elapsed_time

    return {
        "num_blocks": num_blocks,
        "elapsed_time": elapsed_time,
        "avg_cpu_usage": avg_cpu_usage,
        "estimated_energy": estimated_energy
    }

if __name__ == "__main__":
    blockchain = Blockchain()

    NUM_BLOCKS = 10  # Adjust based on desired workload

    energy_results = measure_energy_usage(blockchain, NUM_BLOCKS)

    print(f"Energy Test Results:")
    print(f"- Blocks Mined: {energy_results['num_blocks']}")
    print(f"- Time Taken: {energy_results['elapsed_time']:.2f} sec")
    print(f"- Avg CPU Usage: {energy_results['avg_cpu_usage']:.2f}%")
    print(f"- Estimated Energy Usage: {energy_results['estimated_energy']:.2f} CPU-seconds")
