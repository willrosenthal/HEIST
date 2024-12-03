import time
from solcx import compile_source, install_solc
from web3 import Web3
from utility_functions import basic_error_handling

install_solc('0.8.0')

def deploy_contract(w3, account_proposer, proposer_private_key):
    # Load Solidity contract
    with open('Handshake.sol', 'r') as file:
        contract_source_code = file.read()

    # Compile contract
    compiled_sol = compile_source(contract_source_code, solc_version='0.8.0')
    contract_id, contract_interface = compiled_sol.popitem()

    # Deploy contract
    handshake = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # Build transaction
    nonce = w3.eth.get_transaction_count(account_proposer)
    tx_dict = handshake.constructor().build_transaction({
        'from': account_proposer,
        'nonce': nonce,
        'gas': 5000000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'chainId': 1337  # Ganache's default chain ID
    })

    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx_dict, private_key=proposer_private_key)

    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    handshake_contract = w3.eth.contract(address=contract_address, abi=contract_interface['abi'])

    print(f"Contract deployed at address: {contract_address}")
    return contract_address, handshake_contract

def execute_smart_contract(w3, contract, handshake_contract, account_requester, requester_private_key):
    try:
        nonce = w3.eth.get_transaction_count(account_requester)
        tx_dict = handshake_contract.functions.createContract(
            contract.proposer,
            contract.requester,
            contract.target_type,
            contract.coordinates,
            contract.data_size,
            contract.urgency,
            contract.security_level
        ).build_transaction({
            'from': account_requester,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'chainId': 1337  # Ganache's default chain ID
        })

        signed_tx = w3.eth.account.sign_transaction(tx_dict, private_key=requester_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Get the returned contract ID from the transaction receipt
        tx_logs = handshake_contract.events.ContractCreated().process_receipt(tx_receipt)
        contract_id = tx_logs[0]['args']['id']
        
        print(f"Smart contract execution successful for contract {contract.contract_id} (Blockchain ID: {contract_id}).")
        contract.blockchain_id = contract_id  # Store the blockchain contract ID
        return True
    except Exception as e:
        print(f"Smart contract execution failed: {e}")
        return basic_error_handling(contract)

def validate_node(node):
    # Simulate HandSHAKE verification
    return True  # Assuming validation is successful for simplicity

def health_check_node(node):
    # Check node's online status and bandwidth availability
    print(f"Health check for Node {node.node_id}: Online={node.is_online}, Bandwidth used={node.total_bandwidth_used}/{node.bandwidth}")
    if not node.is_online or (node.total_bandwidth_used >= node.bandwidth):
        return False
    return True