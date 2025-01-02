class DataRequest:
    def __init__(self, request_id, source, destination, data_size, importance, time_sensitivity,
                 security_level, urgency, modulation, datarate, latency_tolerance,
                 coverage_area, encryption, scheduling):
        self.request_id = request_id
        self.source = source
        self.destination = destination
        self.data_size = data_size  # in MB
        self.importance = importance  # Lower value => higher importance
        self.time_sensitivity = time_sensitivity
        self.security_level = security_level  # Lower value => higher security requirement
        self.urgency = urgency  # Lower value => higher urgency
        self.latency = 0
        self.environmental_conditions = "clear"
        # Transmission parameters
        self.modulation = modulation
        self.datarate = datarate
        self.latency_tolerance = latency_tolerance
        self.coverage_area = coverage_area
        self.encryption = encryption
        self.scheduling = scheduling

class SmartContract:
    """
    Represents a contract in the simulation (not the on-chain version directly).
    We store relevant data and track priority, urgency, etc.
    """
    def __init__(self, contract_id, proposer, requester, target_type, coordinates,
                 data_size, priority, deadline, security_level, urgency):
        self.contract_id = contract_id      # Local contract ID (used in simulation)
        self.blockchain_id = None           # Blockchain ID from Handshake.sol
        self.proposer = proposer
        self.requester = requester
        self.target_type = target_type
        self.coordinates = coordinates
        self.data_size = data_size  # in MB
        self.priority = priority    # Derived from importance/urgency
        self.deadline = deadline
        self.security_level = security_level
        self.urgency = urgency

    def __lt__(self, other):
        """
        Define how Python sorts SmartContract objects in a priority queue.
        Lower urgency => processed first, if tie then lower security_level => processed first.
        If tie again, then compare the 'priority' field.
        """
        if self.urgency != other.urgency:
            return self.urgency < other.urgency
        if self.security_level != other.security_level:
            return self.security_level < other.security_level
        return self.priority < other.priority
