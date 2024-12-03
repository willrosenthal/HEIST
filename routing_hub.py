import random
import time
from smart_contract import execute_smart_contract, health_check_node
from utility_functions import log_operator_response
from data_request import SmartContract

class RoutingHub:
    def __init__(self, nodes, w3, handshake_contract, account_requester, requester_private_key):
        self.nodes = nodes
        self.w3 = w3
        self.handshake_contract = handshake_contract
        self.account_requester = account_requester
        self.requester_private_key = requester_private_key

    def route_request(self, data_request, exclude_node=None):
        # Create SmartContract instance
        contract = SmartContract(
            contract_id=random.randint(1000, 9999),
            proposer=self.w3.eth.accounts[0],
            requester=self.account_requester,
            target_type=data_request.source,
            coordinates=f"{data_request.source}-{data_request.destination}",
            data_size=data_request.data_size,
            priority=data_request.importance,
            deadline=data_request.time_sensitivity,
            security_level=data_request.security_level,
            urgency=data_request.urgency
        )
        print(f"\nRouting request {data_request.request_id} from {data_request.source} to {data_request.destination}")
        self.assign_contract(contract, exclude_node=exclude_node)

    def assign_contract(self, contract, exclude_node=None):
        assigned = False
        node = None
        success = execute_smart_contract(
            self.w3,
            contract,
            self.handshake_contract,
            self.account_requester,
            self.requester_private_key
        )
        if not success:
            print(f"Smart contract execution failed for contract {contract.contract_id}.")
            return
        nodes_to_try = [node for node in self.nodes if node != exclude_node and health_check_node(node)]
        if not nodes_to_try:
            print("No nodes are available to accept the contract.")
            return

        # Find nodes with the minimum latency factor
        min_latency = min(n.latency_factor for n in nodes_to_try)
        nodes_with_min_latency = [n for n in nodes_to_try if n.latency_factor == min_latency]

        # Among these nodes, find those with the maximum available bandwidth
        max_available_bandwidth = max(n.bandwidth - n.total_bandwidth_used for n in nodes_with_min_latency)
        candidates = [n for n in nodes_with_min_latency if (n.bandwidth - n.total_bandwidth_used) == max_available_bandwidth]

        # Randomly select one of the candidate nodes
        selected_node = random.choice(candidates)
        if selected_node.accept_contract(contract):
            print(f"Contract {contract.contract_id} successfully assigned to Node {selected_node.node_id}.")
            assigned = True
        else:
            # If selected node couldn't accept the contract, try others
            nodes_to_try.remove(selected_node)
            for node in nodes_to_try:
                if node.accept_contract(contract):
                    print(f"Contract {contract.contract_id} successfully assigned to Node {node.node_id}.")
                    assigned = True
                    break
        if not assigned:
            print(f"Contract {contract.contract_id} could not be assigned due to bandwidth or node failures.")
            log_operator_response(selected_node.node_id if selected_node else None, accepted=False, reason="Bandwidth or node failures")

    def process_all_nodes(self):
        for node in self.nodes:
            node.process_tasks(self)