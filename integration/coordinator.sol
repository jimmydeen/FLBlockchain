// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";


contract Coordinator is Ownable {

    event GlobalModelUpdated(GlobalModel _globalModel);

    struct ModelUpdate {
        string updateHash;
        uint256 numDatapoints;
    }

    struct GlobalModel {
        string modelHash;
        uint32 modelNumber;
    }

    GlobalModel private globalModel;



    mapping(address => ModelUpdate) private modelUpdates;

    function submitUpdate(string memory _updatehash, uint256 _numDatapoints) public {
        ModelUpdate memory update = ModelUpdate(_updatehash, _numDatapoints);
        modelUpdates[msg.sender] = update;

    }

    function updateGlobalModel(GlobalModel memory _globalModel) public onlyOwner {
        globalModel = _globalModel;

        emit GlobalModelUpdated(_globalModel);
    }

    function distributeIncentive(address payable _trainerAddress, uint256 _incentiveAmount) public onlyOwner {
        
    }
    
}