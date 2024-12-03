
# HEIST Simulation Program

## Introduction
The Hybrid Space/Submarine Architecture Ensuring Infosec of Telecommunications (HEIST) is an international consortium aiming to enhance the security and resilience of global telecommunications infrastructure. Given the increasing threats to subsea cables and the critical importance of secure data transfer, HEIST proposes a hybrid architecture combining submarine surveillance, satellite communication, and data rerouting mechanisms to safeguard information flow.

This simulation program serves as a "mini model" representing the HEIST concept. It demonstrates how data requests are managed, how smart contracts facilitate secure communication, and how the system responds to disruptions in primary communication lines by rerouting data through alternative nodes (e.g., satellites), which is a core objective of HEIST.

---

## Prerequisites
To run this simulation, ensure you have the following installed and configured:

### Required Software:
- **Python**: Version 3.8 or higher
- **Ganache**: A personal Ethereum blockchain for development
- **Solidity Compiler (solc)**: Version 0.8.0

### Required Python Packages:
- `web3`
- `py-solc-x`
- `tqdm`
- `cryptography`

---

## Installation

### Step 1: Install Python Packages
Use the following command to install the required Python packages:
```
pip install web3 py-solc-x tqdm colorama cryptography
```

### Step 2: Install Ganache
Download and install Ganache from its [official website](https://trufflesuite.com/ganache). This tool will simulate a local Ethereum blockchain for smart contract deployment and interaction.

### Step 3: Install Solidity Compiler
Install the Solidity compiler version 0.8.0 using `py-solc-x`:
```
python -m solcx.install v0.8.0
```

### Step 4: Configure Ganache
- Start Ganache and ensure it is running on `http://127.0.0.1:7545` (default port).
- Note the accounts and their corresponding private keys provided by Ganache.

---

## Configuration

### Update `main.py` with Accounts and Private Keys
In the `main.py` file, update the `private_keys` dictionary with the accounts and private keys from your Ganache instance:
```
private_keys = {
    '0xYourAccountAddress1': '0xYourPrivateKey1',
    '0xYourAccountAddress2': '0xYourPrivateKey2',
    # Add more accounts as needed
}
```
Ensure all account addresses are in lowercase.

---

## Running the Simulation
Run the simulation by executing the `main.py` script:
```
python main.py
```

### Simulation Workflow:
1. Deploy the Handshake smart contract to the local blockchain.
2. Initialize nodes representing satellites or ground stations.
3. Generate random data requests simulating data needing to be transferred.
4. Route data requests through the system, assigning them to nodes based on various parameters.
5. Process the data transfers, simulating environmental conditions and handling any disruptions.

---

## Functional Requirements Addressed
### FR-01: Detect Disruptions and Reroute
- **Implementation**: The `detect_disruption()` function monitors node statuses. If a node goes offline (e.g., cable cut), the system reroutes data through available nodes.
- **Smart Contracts**: The `execute_smart_contract()` function securely manages rerouting decisions.

### FR-02: Monitor Latency and Bandwidth
- **Implementation**: Nodes track bandwidth usage. The `health_check_node()` function checks node availability and resources before task assignment.

### FR-03: Prioritize Data Streams
- **Implementation**: Data requests have urgency and importance levels. The `Node` class uses a priority queue to ensure higher-priority tasks are processed first.

### FR-04: Integrate HandSHAKE for Verification
- **Implementation**: The `validate_node()` function simulates the HandSHAKE protocol for node identity verification.

### FR-07: Routing Hub Decision Engine
- **Implementation**: The `RoutingHub` class determines the best data paths based on node health, latency, and bandwidth.

### FR-08: Secure Rerouting with Smart Contracts
- **Implementation**: Smart contracts ensure secure rerouting and provide an immutable record of transactions.

---

## Key Performance Parameters
- **Data Size**: Simulates varying data sizes (e.g., 50 MB, 100 MB, 200 MB) to test bandwidth handling.
- **Latency**: Nodes simulate latency based on conditions and urgency.
- **Bandwidth**: Nodes have finite bandwidth capacities, tracked dynamically.
- **Security Compliance**: Communications are managed via smart contracts, ensuring secure and verifiable transactions.
- **Error Handling**: Implements retries and error handling for node operations and smart contracts.
- **Scalability**: Supports additional nodes and requests for testing scalability.

---

## Conclusion
This simulation provides a foundational understanding of the HEIST architecture, demonstrating data rerouting, system resilience, and compliance with performance metrics.
