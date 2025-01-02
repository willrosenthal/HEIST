# situational_awareness_hub.py
import random

class SituationalAwarenessHub:
    """
    The SA Hub monitors cables or network infrastructure participating in HEIST.
    If a disruption is detected, it issues an alert to all interested nodes.
    Once conditions are restored, it notifies the DLR to terminate the contracts.
    """
    def __init__(self):
        self.threat_detected = False
        self.alert_issued = False
        self.restored = False

    def monitor_infrastructure(self):
        """
        Periodically check the infrastructure state (e.g., cables, satellites, etc.).
        Simulate random threat detection and resolution.
        """
        # Randomly decide if a threat arises
        if not self.threat_detected and random.choice([False, True, True]):
            self.threat_detected = True
            self.alert_issued = True
            print("\n[SA Hub] Threat detected! Issuing alerts to all nodes...")

        # If a threat is ongoing, there's a random chance it gets resolved
        elif self.threat_detected and random.choice([False, True]):
            self.threat_detected = False
            self.restored = True
            print("\n[SA Hub] Conditions restored. Signaling DLR to terminate contracts.")

    def issue_alerts(self, all_nodes):
        """
        Sends an alert message to each node in the system.
        """
        if self.alert_issued:
            for node in all_nodes:
                node.receive_alert()
            # Reset after issuing alert
            self.alert_issued = False

    def reset_restored_flag(self):
        """
        Reset the 'restored' state after the DLR has taken action.
        """
        self.restored = False