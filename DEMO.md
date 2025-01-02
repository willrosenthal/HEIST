# HEIST Simulation: Routing Hub – Step-by-Step Summary

Below is a **step-by-step summary** of how each step is realized in the **HEIST** demo, referencing key lines and moments in the logs to show exactly how the simulation fulfills the concept of operations (CONOPS).

---

## Simulation Output Recap (Key Excerpts)

```
...
=== Simulation Cycle 1 ===

[SA Hub] Threat detected! Issuing alerts to all nodes...
[Alert] Node 1 received threat alert from SA Hub.
[Alert] Node 2 received threat alert from SA Hub.
[Alert] Node 3 received threat alert from SA Hub.
[Alert] Node 4 received threat alert from SA Hub.

[RoutingHub] Routing request 1 from GroundStation3 to Satellite2
Smart contract execution successful for contract 3859 (Blockchain ID: 1).
...
Node 4 status: Online=True, Condition=threat_alert
Node 4 initiating handshake for contract 3859
Node 4 passed HandSHAKE validation.
Node 4 bandwidth: 0/1875 (Available: 1875 MB)
[2025-01-02 13:43:23] Operator 4: Accepted rerouting request. Reason: None
Node 4 accepted contract 3859 (Urgency: 2, Priority: 2)
[RoutingHub] Contract 3859 assigned to Node 4
Node 4 is processing contract 3859
Node 4 transferring data: 100%|█████| 200/200 [00:02<00:00, 91.99MB/s]
Node 4 completed processing contract 3859
Logging performance metrics for Node 4, Contract 3859:
Latency: 10000.00 ms, Bandwidth Usage: 200 MB
Node 4 has no tasks to process.

[RoutingHub] Routing request 4 from GroundStation3 to Satellite1
Smart contract execution successful for contract 4956 (Blockchain ID: 2).
...
Node 2 status: Online=True, Condition=threat_alert
Node 2 initiating handshake for contract 4956
Node 2 passed HandSHAKE validation.
...
Node 2 accepted contract 4956 (Urgency: 3, Priority: 4)
[RoutingHub] Contract 4956 assigned to Node 2
[RoutingHub] Continuous log for high-security contract 3859 in progress...
[RoutingHub] Continuous log for high-security contract 4956 in progress...
...
```

### Step-by-Step Explanation (Cycle 1 references)

1. **Step 1: SA Hub Monitors & Detects a Threat**  
   At the start of cycle 1:
   ```
   [SA Hub] Threat detected! Issuing alerts to all nodes...
   [Alert] Node 1 received threat alert...
   [Alert] Node 2 ...
   [Alert] Node 3 ...
   [Alert] Node 4 ...
   ```
   This is the **SA Hub** discovering a disruption and telling each node about it.

2. **Step 2: DRL (RoutingHub) Produces a Smart Contract**  
   Immediately after the alert, we see:
   ```
   [RoutingHub] Routing request 1 from GroundStation3 to Satellite2
   Smart contract execution successful for contract 3859 (Blockchain ID: 1).
   ```
   The DRL creates a new on-chain contract (“3859”), referencing a random `DataRequest`.

3. **Step 3: STE Nodes Receive the Contract**  
   The logs check each node’s health:
   ```
   Health check for Node 1...
   Health check for Node 2...
   Health check for Node 3...
   Health check for Node 4...
   ```
   Node 4 is picked:
   ```
   Node 4 status: Online=True, Condition=threat_alert
   Node 4 initiating handshake for contract 3859
   Node 4 passed HandSHAKE validation.
   ...
   Node 4 accepted contract 3859
   [RoutingHub] Contract 3859 assigned to Node 4
   ```
   This demonstrates the node verifying it can handle the contract (bandwidth, online status) and performing the "handshake."

4. **Step 4: Node Executes the Routing**  
   Right afterward:
   ```
   Node 4 is processing contract 3859
   Node 4 transferring data: 100%|█████| 200/200 [00:02<...]
   Node 4 completed processing contract 3859
   Logging performance metrics for Node 4, Contract 3859:
   Latency: 10000.00 ms, Bandwidth Usage: 200 MB
   ```
   This is the actual data transfer. Node 4’s logs show how it processes the 200 MB payload, measuring latency, etc.

5. **Step 5: Continuous Logging**  
   The output then says:
   ```
   [RoutingHub] Continuous log for high-security contract 3859 in progress...
   ```
   The code treats certain security levels (e.g., `security_level == 1` or a threshold) as “high security.” So we see ongoing logs for the link.

   Later in the same cycle, a second contract (`4956`) is assigned to Node 2. We see a similar log:
   ```
   [RoutingHub] Continuous log for high-security contract 4956 in progress...
   ```

6. **Step 6: Termination**  
   This step typically happens when the SA Hub senses conditions are restored. We see that in a later cycle:
   ```
   [SA Hub] Conditions restored. Signaling DLR to terminate contracts.
   [RoutingHub] Terminating contract 3859 on Node 4 ...
   [RoutingHub] Final log for contract 3859 ...
   [RoutingHub] Terminating contract 4956 on Node 2 ...
   [RoutingHub] Final log for contract 4956 ...
   ```
   That is the DRL halting the active contracts (3859, 4956), producing final logs, and returning the node to normal usage.

---

### Further References in the Log

- **Cycle 2**  
  Node 2 finishes contract 4956:
  ```
  Node 2 is processing contract 4956
  Node 2 transferring data: 100%|█████| 200/200 ...
  Node 2 completed processing contract 4956
  Logging performance metrics...
  ```
  Then a new contract (`8968`) is created and accepted by Node 3:
  ```
  [RoutingHub] Routing request 7 from GroundStation1 to Satellite2
  Smart contract execution successful for contract 8968...
  Node 3 accepted contract 8968 (Urgency: 2, Priority: 3)
  ...
  [RoutingHub] Continuous log for high-security contract 3859 in progress...
  [RoutingHub] Continuous log for high-security contract 4956 in progress...
  ```

- **Cycle 3**  
  The SA Hub indicates:
  ```
  [SA Hub] Conditions restored. Signaling DLR to terminate contracts.
  ```
  So the DRL terminates all active contracts: `3859, 4956, 8968`.
  ```
  [RoutingHub] Terminating contract 3859...
  [RoutingHub] Final log for contract 3859...
  [RoutingHub] Terminating contract 4956...
  [RoutingHub] Final log for contract 4956...
  [RoutingHub] Terminating contract 8968...
  [RoutingHub] Final log for contract 8968...
  ```
  The simulation *still* tries to route a new request (`3614`) afterward:
  ```
  [RoutingHub] Routing request 6 from GroundStation2 to Satellite1
  Smart contract execution successful for contract 3614...
  Node 3 accepted contract 3614 (Urgency: 1, Priority: 3)
  [RoutingHub] Contract 3614 assigned to Node 3
  ```

- **Cycle 4**  
  Another threat is detected:
  ```
  [SA Hub] Threat detected! Issuing alerts to all nodes...
  [Alert] Node 1...
  [Alert] Node 2...
  [Alert] Node 3...
  [Alert] Node 4...
  [RoutingHub] Routing request 1...
  Smart contract execution successful for contract 1523...
  ```
  Node 3 accepts two tasks (`1523` and then finishes `3614`):
  ```
  Node 3 accepted contract 1523...
  Node 3 is processing contract 1523
  ...
  Node 3 completed processing contract 1523
  ...
  Node 3 is processing contract 3614
  Node 3 transferring data: 100%|██████| 50/50...
  Node 3 completed processing contract 3614
  ...
  [RoutingHub] Continuous log for high-security contract 1523 in progress...
  ```

- **Cycle 5**  
  The SA Hub sees conditions restored again:
  ```
  [SA Hub] Conditions restored. Signaling DLR to terminate contracts.
  [RoutingHub] Terminating contract 3614 on Node 3...
  ...
  [RoutingHub] Terminating contract 1523 on Node 3...
  ...
  [RoutingHub] Contract 1587 assigned to Node 4
  ```
  The final lines show Node 4 accepting contract `1587` with updated condition “interference.”

---

## How Each Step Is Reflected in the Logs

1. **SA Hub Monitoring & Threat Alerts**  
     ```
     [SA Hub] Threat detected! Issuing alerts to all nodes...
     [SA Hub] Conditions restored. Signaling DLR to terminate contracts.
     ```

2. **DRL Contract Generation**  
     ```
     [RoutingHub] Routing request X from GroundStationY to SatelliteZ
     Smart contract execution successful for contract XXXX (Blockchain ID: N).
     ```

3. **Nodes (STE Operators) See & Evaluate the Contract**  
     ```
     Node 2 status: Online=True, Condition=threat_alert
     Node 2 initiating handshake for contract 4956
     Node 2 passed HandSHAKE validation.
     Node 2 accepted contract 4956
     ```

4. **Contract Execution**  
     ```
     Node X is processing contract XXXX
     Node X transferring data: 100%|█████| ...
     Node X completed processing contract XXXX
     ```

5. **Continuous Logging for High-Security**  
     ```
     [RoutingHub] Continuous log for high-security contract 3859 in progress...
     [RoutingHub] Continuous log for high-security contract 4956 in progress...
     ```

6. **Termination & Final Logs**  
     ```
     [SA Hub] Conditions restored. Signaling DLR to terminate contracts.
     [RoutingHub] Terminating contract XXXX on Node X ...
     [RoutingHub] Final log for contract XXXX ...
     ```

---

## Conclusion

- **Step 1 & 6**: SA Hub triggers or resolves threats.  
- **Step 2**: RoutingHub generates new contracts upon threat detection.  
- **Step 3**: STE (satellite) nodes accept or reject those contracts.  
- **Step 4**: Accepted contracts are processed (data is transferred).  
- **Step 5**: Higher-security contracts get continuous logs.  
- **Step 6**: Upon “conditions restored,” active contracts are terminated.

Thus, we confirm the simulation thoroughly demonstrates each core concept for the HEIST environment.
````
