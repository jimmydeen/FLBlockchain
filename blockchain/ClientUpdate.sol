// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract ClientUpdate {
    // This is a comment!
    ModelUpdate[] public updates;

    struct ModelUpdate {
        uint256 modelVersion; // Global model version updates are based on
        uint256 timestamp;
        address client; //or client id?
        bytes updateData; //param / gradients
    }

    function submitUpdate(bytes memory _updateData) public {
        // Some validation, make sure msg.sender is allowed to submit updates
        // TO DO
        // Send update to chain
        ModelUpdate memory newUpdate = ModelUpdate({
            modelVersion: 0, // Blank, still undecided if needed
            timestamp: block.timestamp,
            client: msg.sender,
            updateData: _updateData
        });

        updates.push(newUpdate);
        // Maybe Trigger event for detailed information of updates (not sensitive)
    }

    function retrieve() public view returns (bytes memory _updateData) {
        // Gets most recent update data (DEMO ONLY)
        return updates[updates.length - 1].updateData;
    }
}
