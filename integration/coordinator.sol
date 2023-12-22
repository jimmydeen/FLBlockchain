// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";


contract Coordinator is Ownable {

    event GlobalModelUpdated(uint32 modelNumber);

    struct ModelUpdate {
        string updateHash;
        uint256 numDatapoints;
    }

    struct GlobalModel {
        string modelHash;
        uint32 modelNumber;
    }

    GlobalModel private globalModel;
    // List of approved trainers that can submit updates/access global model
    address[] private approvedTrainers;

    // Mapping of latest model update from each trainer
    mapping(address => ModelUpdate) private modelUpdates;

    // For trainer to submit update
    function submitUpdate(string memory _updatehash, uint256 _numDatapoints) public {
        ModelUpdate memory update = ModelUpdate(_updatehash, _numDatapoints);
        modelUpdates[msg.sender] = update;

    }

    // To update global model
    function updateGlobalModel(GlobalModel memory _globalModel) public onlyOwner {
        globalModel = _globalModel;

        emit GlobalModelUpdated(_globalModel);
    }

    // To send incentive to trainer
    function distributeIncentive(address payable _trainerAddress, uint256 _incentiveAmount) public onlyOwner {

    }
    
}