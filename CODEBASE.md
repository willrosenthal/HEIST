# HEIST Codebase

This document provides an **in-depth explanation** of how all the pieces of the HEIST codebase work together to create the final simulation results. We’ll highlight specific lines or segments from each file to show how they impact routing decisions, data requests, environmental conditions, and more.

---

## 1. `main.py` (Main Entrypoint)

**Purpose:**  
- Initializes the Ethereum/Web3 connection.  
- Deploys the `Handshake.sol` contract.  
- Creates `Node` objects and the `RoutingHub`.  
- Contains the main simulation loop where the **Situational Awareness Hub** (SA Hub) and **Routing Hub** logic unfold.

**Key Sections:**  
- **Lines ~25–30**: Connect to Ganache via `Web3(HTTPProvider('http://127.0.0.1:7545'))`, inject the `ExtraDataToPOAMiddleware`, and get `w3.eth.accounts`.  
- **Lines ~39–44**: Deploys the contract using `deploy_contract(...)` from `smart_contract.py`.  
- **Lines ~46–60**: Instantiates `Node` objects in a loop. Each node is assigned a random bandwidth and an associated Ethereum account with a matching private key (if available).  
- **Lines ~62–63**: Creates the `RoutingHub` and the `SituationalAwarenessHub` objects.  
- **Lines ~66–84**: Generates a list of random `DataRequest` instances. Each request has fields like `data_size`, `importance`, `security_level`, etc.  
- **Lines ~86–120**: **Main simulation loop** (e.g., 5 cycles):
  1. **SA Hub checks for threats** (`monitor_infrastructure()`).
  2. If a threat is found, alerts are issued to nodes, and **one** data request is routed (`routing_hub.route_request(req)`).
  3. If the SA Hub says conditions are restored, `routing_hub.terminate_contract(cid)` is called for all active contracts.
  4. Nodes update environmental conditions (`node.update_environment_conditions()`).
  5. `routing_hub.process_all_nodes()` to let each node handle tasks.
  6. Continuous logging (`log_high_classification_traffic`) on any high-security contracts.
  7. `detect_disruption(...)` from `utility_functions.py` to handle offline nodes or other disruptions.

**Impact:**  
- The main loop triggers new requests primarily when the SA Hub detects a threat.  
- Can add or modify logic here to generate additional traffic, alter threat detection probability, or skip termination.  
- Each cycle, the environment is updated (storms, solar flares, etc.) for each node, affecting availability and latency factors.

---

## 2. `smart_contract.py`

**Purpose:**  
- Responsible for compiling & deploying `Handshake.sol`.  
- Provides functions to **execute** a new smart contract on-chain (`execute_smart_contract(...)`).  
- Checks node health/validation in simplified form.

**Key Sections:**  
- **Lines ~12–20**: `deploy_contract(...)` loads and compiles `Handshake.sol`, then deploys it to Ganache.  
- **Lines ~22–60**: `execute_smart_contract(...)` interacts with the on-chain contract, calling `createContract(...)` in `Handshake.sol`. It signs and sends a transaction from the `requester`.  
- **Line ~70**: `validate_node(node)` is a placeholder for the “HandSHAKE” validation logic.  
- **Line ~78**: `health_check_node(node)` checks if `node.is_online` and if its `total_bandwidth_used` is below `node.bandwidth`.

**Impact:**  
- Successful execution means a new on-chain record is created (the DRL contract).  
- If execution fails, the code triggers `basic_error_handling` in `utility_functions.py`, which retries.  
- The function `health_check_node(node)` helps the `RoutingHub` skip unhealthy or over-capacity nodes.

---

## 3. `Handshake.sol` (Solidity Contract)

**Purpose:**  
- The on-chain component that tracks each contract’s state (proposer, requester, data size, security, etc.).  
- Provides methods like `createContract(...)`, `updateContractData(...)`.

**Key Functions:**  
- **`createContract(...)`**: Increases `contractCount`, stores contract data in `contracts[contractCount]`, and emits a `ContractCreated` event.  
- **`updateContractData(...)`**: Allows you to emit changes for an active contract.  
- **`getContract(...)`**: Retrieves details about a specific contract.

**Impact:**  
- Each time `RoutingHub` calls `execute_smart_contract(...)`, this contract logs a `ContractCreated` event.  
- Could be extended to mark contracts as ended or inactive if the conditions are restored.

---

## 4. `routing_hub.py`

**Purpose:**  
- The **Dynamic Routing Layer (DRL)** logic.  
- Routes new requests by creating a local `SmartContract` object, calling on-chain methods, and assigning a node.

**Key Sections:**  
- **Lines ~10–20**: Constructor stores references to `nodes`, the `handshake_contract`, `account_requester` (for transactions), and creates `self.active_contracts` to track ongoing deals.  
- **Lines ~22–47**: `route_request(data_request)`:  
  1. Wraps the data request into a `SmartContract` object (see `data_request.py`).  
  2. Calls `assign_contract(...)`.  
- **Lines ~49–100**: `assign_contract(...)`:  
  1. Executes the smart contract on-chain using `execute_smart_contract`.  
  2. Calls `health_check_node` on each node to filter out offline or maxed-out nodes.  
  3. Chooses the node with the **lowest `latency_factor`** and highest **available bandwidth**.  
  4. Calls `node.accept_contract(contract)`. If accepted, the contract is stored in `self.active_contracts`.  
- **Lines ~102–112**: `process_all_nodes()`: each node processes its tasks.  
- **Lines ~114–123**: `log_high_classification_traffic(...)`: for security-level=1 (or some threshold).  
- **Lines ~125–145**: `terminate_contract(contract_id)`: halts a contract, frees up node bandwidth (which was removed for simulation purposes), and logs final output.

**Impact:**  
- Determines *which* node gets a contract (`assign_contract`).  
- Tracks all active contracts, meaning the DRL can forcibly terminate them if the SA Hub says conditions are restored.  
- Logs performance or security status as needed.

---

## 5. `node.py`

**Purpose:**  
- Represents an **STE operator** or a single “node” in the network.  
- Holds bandwidth capacity, is subject to environment changes (storms, solar flares), and processes tasks in a queue.

**Key Sections:**  
- **Lines ~28–40**: Constructor sets `node_id`, `bandwidth`, `is_online`, `latency_factor`, etc. Also tracks environment updates with a random interval.  
- **Lines ~42–48**: `receive_alert()`: called by the SA Hub to set `condition = "threat_alert"`, increasing `latency_factor`.  
- **Lines ~50–65**: `handshake(...)`: verifies the node passes `validate_node(...)` from `smart_contract.py`.  
- **Lines ~67–88**: `accept_contract(...)`:
  1. Checks if the node is online and if handshake is successful.  
  2. Verifies available bandwidth is sufficient.  
  3. Pushes the contract into `self.current_tasks` (a min-heap sorted by `contract.priority`).  
- **Lines ~90–110**: `process_tasks(...)`:  
  1. Pops tasks in ascending priority (lowest integer means highest priority).  
  2. Simulates data transfer with a `tqdm` progress bar.  
  3. Logs performance metrics for each completed contract.  
  4. If the node goes offline mid-task, it reroutes the contract to the `RoutingHub`.  
- **Lines ~112–126**: `update_environment_conditions()`: periodically sets `condition` to `storm`, `interference`, `solar_flare`, or `clear`. Each condition may alter `latency_factor` or set `is_online=False`.

**Impact:**  
- The node may become offline or severely degraded if storms or flares are triggered (see `update_environment_conditions`).  
- If the node runs out of bandwidth or fails handshake, it cannot accept new contracts.  
- `priority`/`urgency` determines the processing order of tasks.

---

## 6. `situational_awareness_hub.py`

**Purpose:**  
- The **SA Hub** that detects threats, issues alerts to all nodes, and signals when conditions are restored.

**Key Sections:**  
- **Lines ~10–31**:  
  - `monitor_infrastructure()`: randomly toggles `threat_detected` or `restored`.  
  - `issue_alerts(...)`: calls `node.receive_alert()`.  
  - When `self.restored` is `True`, the DRL is expected to terminate contracts.  

**Impact:**  
- The SA Hub’s detection events drive the creation and termination of contracts in the **main loop** (`main.py`).  
- Alerts trigger the nodes’ “threat_alert” status, which can raise latency or degrade performance.

---

## 7. `utility_functions.py`

**Purpose:**  
- Holds various helper methods for logging, disruption detection, error handling, etc.

**Key Sections:**  
- **Lines ~5–18**: `detect_disruption(nodes, routing_hub)`: if a node is offline, re-route its contracts.  
- **Lines ~20–44**: `basic_error_handling(contract)`: retry logic if a contract deployment fails.  
- **Lines ~46–60**: `log_operator_response(...)` and `log_performance_metrics(...)`: prints acceptance or refusal logs, plus usage stats.  

**Impact:**  
- If a node becomes offline mid-processing, `detect_disruption` tries to re-route the tasks.  
- `basic_error_handling` can salvage a failed contract creation attempt, meaning the DRL can recover from on-chain or connectivity errors.

---

## 8. `data_request.py`

**Purpose:**  
- Defines the `DataRequest` class (incoming requests from end users or operators).  
- Defines the `SmartContract` class used by the DRL for sorting and priority logic.

**Key Sections:**  
- **Lines ~3–24**: `DataRequest` constructor sets fields like `source`, `destination`, `data_size`, `importance`, etc.  
- **Lines ~26–48**: `SmartContract` constructor plus `__lt__` method:
  - `__lt__` ensures tasks are sorted first by `urgency`, then by `security_level`, then by `priority` (importance).  
  - Used by the node’s priority queue in `process_tasks(...)`.

**Impact:**  
- The DRL references `DataRequest` to figure out what source/destination is needed, how big the data load is, and how urgent or secure it is.  
- The nodes rely on `SmartContract.__lt__` to decide which task to process first if multiple tasks are queued.

---

## Putting It All Together

1. **`main.py`** orchestrates everything: deploying the contract, creating the nodes, and looping through cycles to trigger the SA Hub’s threats/restorations.  
2. **`situational_awareness_hub.py`** controls the threat status, alerting nodes to switch to “threat_alert” mode.  
3. **`routing_hub.py`** (DRL) creates on-chain records in `Handshake.sol`, picks healthy nodes, and logs continuous traffic if security level is high.  
4. **`node.py`** decides whether to accept or reject a contract based on bandwidth, online status, and handshake validation.  
5. **`utility_functions.py`** handles retry logic, performance logs, and disruption detection (re-routing if a node goes offline).  
6. **`smart_contract.py`** contains the code to compile/deploy the Solidity contract, plus functions like `execute_smart_contract(...)` that sign and send transactions.  
7. **`Handshake.sol`** is the deployed contract on Ganache, storing each contract’s data and emitting blockchain events.  
8. **`data_request.py`** defines how requests and local `SmartContract` objects are structured, including the sorting logic (urgency, security, priority).

Overall, **routing decisions** hinge on:

- **Node Health** (`is_online`), updated in `update_environment_conditions()`.
- **Bandwidth** (`bandwidth - total_bandwidth_used`).
- **Latency Factor** (increased if storms/interference are set).
- **Urgency & Security** levels of each request (`SmartContract.__lt__`).
