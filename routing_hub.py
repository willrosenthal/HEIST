import random
from smart_contract import execute_smart_contract, health_check_node
from utility_functions import log_operator_response, log_performance_metrics
from data_request import SmartContract

class RoutingHub:
    def __init__(self, nodes, w3, handshake_contract, account_requester, requester_private_key):
        self.nodes = nodes
        self.w3 = w3
        self.handshake_contract = handshake_contract
        self.account_requester = account_requester
        self.requester_private_key = requester_private_key
        self.active_contracts = {}  # Keep track of currently active contracts: {contract_id: {contract, assigned_node}}

    def route_request(self, data_request, exclude_node=None):
        """
        Main entry point for routing a new request. Creates a SmartContract instance, 
        then calls assign_contract() to push it out to a node.
        """
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
        print(f"\n[RoutingHub] Routing request {data_request.request_id} from {data_request.source} to {data_request.destination}")
        self.assign_contract(contract, exclude_node=exclude_node)

    def assign_contract(self, contract, exclude_node=None):
        """
        Execute the smart contract on-chain, then find a suitable node 
        based on latency factor and available bandwidth.
        """
        success = execute_smart_contract(
            self.w3,
            contract,
            self.handshake_contract,
            self.account_requester,
            self.requester_private_key
        )
        if not success:
            print(f"[RoutingHub] Smart contract execution failed for contract {contract.contract_id}.")
            return

        # Filter out node to exclude, plus check for health
        nodes_to_try = [n for n in self.nodes if n != exclude_node and health_check_node(n)]
        if not nodes_to_try:
            print("[RoutingHub] No nodes are available to accept the contract.")
            return

        # Among healthy nodes, find min latency factor
        min_latency = min(n.latency_factor for n in nodes_to_try)
        nodes_with_min_latency = [n for n in nodes_to_try if n.latency_factor == min_latency]

        # Among those, find max available bandwidth
        max_available_bandwidth = max(n.bandwidth - n.total_bandwidth_used for n in nodes_with_min_latency)
        candidates = [n for n in nodes_with_min_latency if (n.bandwidth - n.total_bandwidth_used) == max_available_bandwidth]

        selected_node = random.choice(candidates)
        if selected_node.accept_contract(contract):
            print(f"[RoutingHub] Contract {contract.contract_id} assigned to Node {selected_node.node_id}")
            self.active_contracts[contract.contract_id] = {
                'contract': contract,
                'assigned_node': selected_node
            }
        else:
            # fallback approach: try others in nodes_to_try
            nodes_to_try.remove(selected_node)
            assigned = False
            for node in nodes_to_try:
                if node.accept_contract(contract):
                    print(f"[RoutingHub] Contract {contract.contract_id} assigned to Node {node.node_id}")
                    self.active_contracts[contract.contract_id] = {
                        'contract': contract,
                        'assigned_node': node
                    }
                    assigned = True
                    break

            if not assigned:
                print(f"[RoutingHub] Contract {contract.contract_id} could not be assigned.")
                log_operator_response(selected_node.node_id if selected_node else None,
                                      accepted=False,
                                      reason="Bandwidth or node failures")

    def process_all_nodes(self):
        """
        Let each node process tasks in its queue.
        """
        for node in self.nodes:
            node.process_tasks(self)

    def log_high_classification_traffic(self, contract):
        """
        If this contract is very sensitive (lower security_level => higher classification),
        we do continuous or specialized logging.
        """
        if contract.security_level == 1:
            print(f"[RoutingHub] Continuous log for high-security contract {contract.contract_id} in progress...")

    def terminate_contract(self, contract_id):
        """
        Called when SA Hub indicates conditions are restored, or the user no longer needs the link.
        Removes the contract from the assigned node and optionally updates on-chain state.
        """
        if contract_id not in self.active_contracts:
            return

        contract_info = self.active_contracts[contract_id]
        assigned_node = contract_info['assigned_node']
        contract = contract_info['contract']

        # "Halt" the link – for a real solution, you'd have more robust close-out logic
        print(f"[RoutingHub] Terminating contract {contract_id} on Node {assigned_node.node_id} due to restoration.")
        # assigned_node.total_bandwidth_used = max(0, assigned_node.total_bandwidth_used - contract.data_size)

        print(f"[RoutingHub] Final log for contract {contract.contract_id} has been produced by Node {assigned_node.node_id}.")
        del self.active_contracts[contract_id]
