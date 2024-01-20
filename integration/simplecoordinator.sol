// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract SimpleCoordinator is Ownable {
    event UpdateSubmitted(address indexed _trainer, int256 indexed _numDatapoints, int256 indexed _reward);
    int256 public incentivePerDatapoint;
    int16 public numberUpdatesRequested;
    int256 public maxDataPoints;

    constructor(int256 _incentive, int16 _numberUpdatesRequested, int256 _maxDataPoints) payable {
        setIncentive(_incentive);
        numberUpdatesRequested = _numberUpdatesRequested;
        maxDataPoints = _maxDataPoints;
        // Ensure contract has enough balance for maximum number of data points requested
        require(msg.value >= (incentivePerDatapoint * (maxDataPoints)), "Not enough deposit");
        
    }

    function setIncentive(int256 _incentive) public onlyOwner {
        incentivePerDatapoint = _incentive;
    }
    function submitUpdate(int256 _numDatapoints) public payable {
        int256 reward = (_numDatapoints * (incentivePerDatapoint)) / (numberUpdatesRequested);
        require(address(this).balance >= reward, "Not enough balance");
        payable(msg.sender).transfer(reward);
        emit UpdateSubmitted(msg.sender, _numDatapoints, reward);
    }

    function distributeIncentive(address _trainer) {

    }
}