// Handshake.sol
pragma solidity ^0.8.0;

contract Handshake {
    uint256 public contractCount = 0;

    struct Contract {
        uint256 id;
        address proposer;
        address requester;
        string targetType;
        string coordinates;
        uint256 dataSize;
        uint256 urgency;
        uint256 securityLevel;
        bool isActive;
    }

    mapping(uint256 => Contract) public contracts;

    event ContractCreated(
        uint256 id,
        address proposer,
        address requester,
        string targetType,
        string coordinates,
        uint256 dataSize,
        uint256 urgency,
        uint256 securityLevel
    );

    event ContractUpdated(uint256 id, string data);

    function createContract(
        address proposer,
        address requester,
        string memory targetType,
        string memory coordinates,
        uint256 dataSize,
        uint256 urgency,
        uint256 securityLevel
    ) public returns (uint256) {
        contractCount++;
        contracts[contractCount] = Contract(
            contractCount,
            proposer,
            requester,
            targetType,
            coordinates,
            dataSize,
            urgency,
            securityLevel,
            true
        );
        emit ContractCreated(
            contractCount,
            proposer,
            requester,
            targetType,
            coordinates,
            dataSize,
            urgency,
            securityLevel
        );
        return contractCount;
    }

    function getContract(uint256 id)
        public
        view
        returns (
            uint256,
            address,
            address,
            string memory,
            string memory,
            uint256,
            uint256,
            uint256,
            bool
        )
    {
        Contract memory c = contracts[id];
        return (
            c.id,
            c.proposer,
            c.requester,
            c.targetType,
            c.coordinates,
            c.dataSize,
            c.urgency,
            c.securityLevel,
            c.isActive
        );
    }

    function updateContractData(uint256 id, string memory data) public {
        require(contracts[id].isActive, "Contract is not active");
        emit ContractUpdated(id, data);
    }
}
