// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import {Ownable} from "/Users/jd/Desktop/work/FLBlockchain/integration/Ownable.sol";

contract SimpleCoordinator is Ownable(msg.sender) {
    event UpdateSubmitted(address indexed _trainer, uint256 indexed _numDatapoints, uint256 indexed _reward);
    event IncentiveDistributed(address indexed _trainer, uint256 indexed _reward);
    uint256 public incentivePerDatapoint;
    uint16 public numberUpdatesRequested;
    uint256 public maxDataPoints;

    constructor(uint256 _incentiveInWei, uint16 _numberUpdatesRequested, uint256 _maxDataPoints) payable {
        setIncentive(_incentiveInWei);
        numberUpdatesRequested = _numberUpdatesRequested;
        maxDataPoints = _maxDataPoints;
        // Ensure contract has enough balance for maximum number of data points requested
        require(msg.value >= (incentivePerDatapoint * (maxDataPoints)), "Not enough deposit");
        
    }

    function setIncentive(uint256 _incentiveInWei) public onlyOwner {
        incentivePerDatapoint = _incentiveInWei;
    }

    function submitUpdate(uint256 _numDatapoints) public payable {
        submitUpdate(_numDatapoints, 0);
    }
    function submitUpdate(uint256 _numDatapoints, uint256 _gasEstimate) public payable {
        // Calculate reward
        uint256 reward = (_numDatapoints * (incentivePerDatapoint)) / (numberUpdatesRequested) + _gasEstimate;
        // Send reward to trainer via distributeIncentive
        distributeIncentive(msg.sender, reward);
        emit UpdateSubmitted(msg.sender, _numDatapoints, reward);
    }

    function distributeIncentive(address _trainer, uint256 rewardAmount) private {
        require(address(this).balance >= rewardAmount, "Not enough balance");
        payable(_trainer).transfer(rewardAmount);
        emit IncentiveDistributed(_trainer, rewardAmount);


    }
}