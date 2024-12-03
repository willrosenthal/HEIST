import time
import heapq
import random
from utility_functions import log_operator_response, log_performance_metrics
from smart_contract import validate_node
from tqdm import tqdm
from colorama import init, Fore, Style

init(autoreset=True)

class Node:
    def __init__(self, node_id, bandwidth, w3, contract, account, private_key):
        self.node_id = node_id
        self.bandwidth = bandwidth  # Total bandwidth capacity in MB
        self.latency_factor = 1.0
        self.current_tasks = []
        self.total_bandwidth_used = 0
        self.is_online = True
        self.condition = "clear"
        self.w3 = w3
        self.contract = contract
        self.account = account
        self.private_key = private_key
        self.condition_update_interval = random.uniform(10, 20)  # Update every 10-20 seconds
        self.last_condition_update = time.time()

    def handshake(self, contract):
        print(f"Node {self.node_id} initiating handshake for contract {contract.contract_id}")
        if not validate_node(self):
            print(f"Node {self.node_id} failed HandSHAKE validation.")
            return False
        print(f"Node {self.node_id} passed HandSHAKE validation.")
        return True

    def accept_contract(self, contract):
        print(f"Node {self.node_id} status: Online={self.is_online}, Condition={self.condition}")
        if not self.is_online:
            print(Fore.RED + f"Node {self.node_id} is offline due to {self.condition}. Cannot accept contract {contract.contract_id}.")
            return False
        if not self.handshake(contract):
            print(Fore.RED + f"Node {self.node_id} failed to establish secure communication for contract {contract.contract_id}.")
            return False
        available_bandwidth = self.bandwidth - self.total_bandwidth_used
        print(f"Node {self.node_id} bandwidth: {self.total_bandwidth_used}/{self.bandwidth} (Available: {available_bandwidth} MB)")
        if self.total_bandwidth_used + contract.data_size > self.bandwidth:
            print(Fore.RED + f"Node {self.node_id} cannot accept contract {contract.contract_id} due to bandwidth limitations.")
            return False
        heapq.heappush(self.current_tasks, (contract.priority, contract))
        self.total_bandwidth_used += contract.data_size
        log_operator_response(self.node_id, accepted=True)
        print(Fore.GREEN + f"Node {self.node_id} accepted contract {contract.contract_id} (Urgency: {contract.urgency}, Priority: {contract.priority})")
        return True

    def process_tasks(self, routing_hub):
        while self.current_tasks:
            _, contract = heapq.heappop(self.current_tasks)
            if not self.is_online:
                print(Fore.RED + f"Node {self.node_id} went offline while processing contract {contract.contract_id}.")
                self.reroute_contract(contract, routing_hub)
                return
            print(f"Node {self.node_id} is processing contract {contract.contract_id}")
            self.visualize_transfer(contract.data_size)
            print(f"Node {self.node_id} completed processing contract {contract.contract_id}")
            log_performance_metrics(self.node_id, contract)
        else:
            print(f"Node {self.node_id} has no tasks to process.")

    def reroute_contract(self, contract, routing_hub):
        print(Fore.YELLOW + f"Node {self.node_id} is rerouting contract {contract.contract_id} due to communication disruption.")
        routing_hub.route_request(contract, exclude_node=self)

    def visualize_transfer(self, data_size):
        # Simulate data transfer with progress bar
        for _ in tqdm(range(data_size), desc=Fore.BLUE + f"Node {self.node_id} transferring data", unit='MB', ncols=70):
            time.sleep(0.01)

    def update_environment_conditions(self):
        current_time = time.time()
        if current_time - self.last_condition_update >= self.condition_update_interval:
            self.last_condition_update = current_time
            self.condition_update_interval = random.uniform(10, 20)
            conditions = ["clear"] * 5 + ["storm", "interference", "solar_flare"]
            self.condition = random.choice(conditions)
            if self.condition == "storm":
                self.is_online = True
                self.latency_factor = 2.0
            elif self.condition == "interference":
                self.is_online = True
                self.latency_factor = 1.5
            elif self.condition == "solar_flare":
                self.is_online = random.choice([True, True, True, False])  # 25% chance to go offline
                self.latency_factor = float('inf') if not self.is_online else 1.0
            else:
                self.is_online = True
                self.latency_factor = 1.0
            print(f"Node {self.node_id} updated condition: {self.condition}, Online: {self.is_online}")