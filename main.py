import time
import random
from node import Node
from data_request import DataRequest
from routing_hub import RoutingHub
from utility_functions import detect_disruption
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from smart_contract import deploy_contract

def simulate():
    # Connect to Ethereum client
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Ensure this matches your Ganache port
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # Get accounts from Ganache
    accounts = w3.eth.accounts

    # Create a mapping of account addresses to private keys (all addresses in lowercase)
    private_keys = {
        '0x2b322409c4f3ac1e7b9bb059c0c52e0134a69934': '0x2f62906a0ea166787a531bf39719d0efb1c8c335ca202731d9bee022b8a84860',
        '0x29e1f9e7d7960b8e7b9ad5c7ea4339be0308c9f8': '0x85cec0001b6aac76ff7fdccba543407a75dd63f5792c2a2c41c1a1788cac4bbd',
        '0x6fd7ec6ec104609a2607244e6c5847af436f607e': '0x63afbaecba43bc82cc2816731bea2e47d8d12e023de3937f5866ae528367e8a1',
        '0xa69f5bca5be2cb55ce9cd895b9a07583f775665c': '0xe36a7867cd655612fca9645091d5b5a1f6fab47d02956a9bb2f2e0026bde7841',
        '0x81735d824d81c0a66bd530b6b03c6594ba826d57': '0xde6171ab96535bf9d3291366f0be5052ed8652cbd8eac03cb1e8eeeedaebf418',
    }

    # Assign proposer and requester accounts
    account_proposer = accounts[0]
    account_requester = accounts[1]

    # Retrieve private keys, ensuring addresses are lowercase
    proposer_private_key = private_keys.get(account_proposer.lower())
    requester_private_key = private_keys.get(account_requester.lower())

    if not proposer_private_key or not requester_private_key:
        print("Proposer or requester private key not found.")
        return

    # Deploy the smart contract
    contract_address, handshake_contract = deploy_contract(w3, accounts[0], proposer_private_key)

    # Initialize nodes
    nodes = []
    for i in range(2, len(accounts)):
        node_account = accounts[i].lower()
        node_private_key = private_keys.get(node_account)
        if not node_private_key:
            print(f"Private key for account {accounts[i]} not found.")
            continue
        node = Node(
            node_id=i-1,
            bandwidth=random.randint(1000, 5000),
            w3=w3,
            contract=handshake_contract,
            account=accounts[i],
            private_key=node_private_key
        )
        nodes.append(node)

    # Initialize the routing hub
    routing_hub = RoutingHub(nodes, w3, handshake_contract, accounts[1], requester_private_key)

    # Generate random data requests
    data_requests = [
        DataRequest(
            request_id=i,
            source="GroundStation{}".format(random.randint(1, 3)),
            destination="Satellite{}".format(random.randint(1, 3)),
            data_size=random.choice([50, 100, 200]),
            importance=random.randint(1, 5),
            time_sensitivity=random.choice(["urgent", "normal", "no urgency"]),
            security_level=random.randint(1, 3),
            urgency=random.randint(1, 3),
            modulation=random.choice(["BPSK", "QPSK", "8-QAM", "16-QAM"]),
            datarate=random.choice(["0-10mbps", "10-100mbps", ">100mbps"]),
            latency_tolerance=random.choice(["<600ms", "<300ms", "<150ms"]),
            coverage_area=random.choice(["SISO", "SIMO", "MIMO"]),
            encryption=random.choice(["AES/GCM-128", "AES/GCM-256", "CARIBOU/CARDHOLDER"]),
            scheduling=random.choice(["No Urgency (<3 hours)", "Urgent (<30 mins)", "Continuous link"])
        ) for i in range(1, 11)
    ]

    # Route each data request and process nodes
    for request in data_requests:
        # Update environmental conditions for all nodes
        for node in nodes:
            node.update_environment_conditions()
        routing_hub.route_request(request)
        routing_hub.process_all_nodes()
        time.sleep(1)

    # Detect disruptions
    detect_disruption(nodes, routing_hub)

# Run simulation
if __name__ == "__main__":
    simulate()