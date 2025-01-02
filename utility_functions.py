import time
import random

def detect_disruption(nodes, routing_hub):
    """
    Detect if any node is offline and re-route its contracts.
    """
    print("\nDetecting disruptions...")
    for node in nodes:
        if not node.is_online:
            print(f"Disruption detected: Node {node.node_id} is offline.")
            # Re-route the contracts in that node's queue
            for task in node.current_tasks:
                _, contract = task
                routing_hub.route_request(contract, exclude_node=node)

def basic_error_handling(contract):
    """
    If a smart contract execution fails, attempt a few retries.
    """
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
        try:
            print(f"Retrying smart contract execution for contract {contract.contract_id} (Attempt {retry_count + 1})...")
            time.sleep(0.5)
            # Randomly decide if the retry succeeds
            if random.choice([True, False]):
                print(f"Smart contract execution successful on retry for contract {contract.contract_id}.")
                return True
            else:
                raise Exception("Simulated smart contract error on retry")
        except Exception as e:
            print(f"Retry {retry_count + 1} failed: {e}")
            retry_count += 1
    print(f"All retries failed for contract {contract.contract_id}.")
    return False

def log_operator_response(operator_id, accepted, reason=None):
    """
    Log whether an operator accepted or refused a contract.
    """
    operator = f"Operator {operator_id}" if operator_id is not None else "No Operator"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    status = "Accepted" if accepted else "Refused"
    print(f"[{timestamp}] {operator}: {status} rerouting request. Reason: {reason}")

def log_performance_metrics(node_id, contract):
    """
    Log performance metrics after a contract is processed.
    Example: latency, bandwidth usage, etc.
    """
    # Simplified placeholder calculation
    latency = (contract.data_size / (contract.urgency * 10)) * 1000  # ms
    bandwidth_usage = contract.data_size
    print(f"Logging performance metrics for Node {node_id}, Contract {contract.contract_id}:")
    print(f"Latency: {latency:.2f} ms, Bandwidth Usage: {bandwidth_usage} MB")

def health_check_node(node):
    """
    Duplicate or simplified version of the function in smart_contract.py for demonstration.
    Keeps the code self-contained.
    """
    print(f"Health check for Node {node.node_id}: Online={node.is_online}, "
          f"Bandwidth used={node.total_bandwidth_used}/{node.bandwidth}")
    if not node.is_online or (node.total_bandwidth_used >= node.bandwidth):
        return False
    return True
