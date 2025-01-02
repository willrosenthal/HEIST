# main.py
import time
import random
from node import Node
from data_request import DataRequest
from routing_hub import RoutingHub
from utility_functions import detect_disruption
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from smart_contract import deploy_contract
from situational_awareness_hub import SituationalAwarenessHub

def simulate():
    # Connect to Ethereum client (Ganache)
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Update host/port if needed
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # Retrieve accounts from Ganache
    accounts = w3.eth.accounts

    # Map addresses to private keys
    private_keys = {
        '0x1458318CE242d8eD8aedfedD013FD76135ceCD51': '0x2a248cba479646350341057f13952c08b811aef3457e053d9ac6b6b70c5e1184',
        '0x3Ed5D636F4bF3590Eb6402cD677cf633dEb4275E': '0x31482f234bc8acfb5360194c0c0d01cd8f947f60c7b523bc2320401dd993d1f9',
        '0xc9D947A27975375bbe584abF769335Ea70bDf1C2': '0xd7222dae1c9fcdba8f16a9b58736a442c1d91194c826afdbff4948a3ac490080',
        '0xcFbC4df8F73B5198f3999b9aB07Bd00BB36e9b1B': '0x7523748cb1c2001123a25b8c2d8f4b82a6af8bd37b82be3ba88319c38f49a75c',
        '0xBAB7C243F8c2234d68058E2C3e8582915D129d9d': '0xb9aeb92b326934eced859384a4b1f828bb44adb50b59d5fa0eb6ecf82e5adebd',
        '0xC56b992d7c51b6a0c0a0adb03B8601070a6f2E57': '0x3f3dcc6e98448c4b2ee960283b3439d72c8aa8edca36f5e0cbb62afcd46cc74f',
    }

    # Assign proposer and requester
    account_proposer = accounts[0]
    account_requester = accounts[1]

    # Get matching private keys
    proposer_private_key = private_keys.get(account_proposer)
    requester_private_key = private_keys.get(account_requester)

    if not proposer_private_key or not requester_private_key:
        print("Proposer or requester private key not found.")
        return

    # Deploy the Solidity contract
    contract_address, handshake_contract = deploy_contract(w3, account_proposer, proposer_private_key)

    # Initialize nodes
    nodes = []
    for i in range(2, len(accounts)):
        node_account = accounts[i]
        node_private_key = private_keys.get(node_account)
        if not node_private_key:
            print(f"Private key for account {accounts[i]} not found.")
            continue

        node = Node(
            node_id=i-1,
            bandwidth=random.randint(1000, 2500),
            w3=w3,
            contract=handshake_contract,
            account=accounts[i],
            private_key=node_private_key
        )
        nodes.append(node)

    # Create the RoutingHub
    routing_hub = RoutingHub(nodes, w3, handshake_contract, account_requester, requester_private_key)

    # Create the Situational Awareness Hub
    sa_hub = SituationalAwarenessHub()

    # Generate some random data requests
    data_requests = [
        DataRequest(
            request_id=i,
            source=f"GroundStation{random.randint(1,3)}",
            destination=f"Satellite{random.randint(1,3)}",
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

    # Main simulation loop
    # Adjust range as desired for more/less cycles
    for cycle in range(1, 6):
        print(f"\n=== Simulation Cycle {cycle} ===")

        # Step 1: The SA Hub checks the infrastructure
        sa_hub.monitor_infrastructure()

        # If a new threat is detected, issue alerts and possibly route a request
        if sa_hub.alert_issued:
            sa_hub.issue_alerts(nodes)

            # For demonstration, route a random user request upon threat detection
            req = random.choice(data_requests)
            routing_hub.route_request(req)

        # If the SA Hub says conditions are restored, terminate active contracts
        if sa_hub.restored:
            active_contract_ids = list(routing_hub.active_contracts.keys())
            for cid in active_contract_ids:
                routing_hub.terminate_contract(cid)

            sa_hub.reset_restored_flag()

        # Let each node process tasks
        for node in nodes:
            node.update_environment_conditions()
        routing_hub.process_all_nodes()

        if random.random() < 0.75:
            req = random.choice(data_requests)
            routing_hub.route_request(req)

        # If there are any high-security contracts, log them
        for cinfo in routing_hub.active_contracts.values():
            contract = cinfo['contract']
            routing_hub.log_high_classification_traffic(contract)

        # Run disruption detection
        detect_disruption(nodes, routing_hub)

        # Delay between simulation cycles (optional)
        time.sleep(1)

if __name__ == "__main__":
    simulate()
