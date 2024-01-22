// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import {Ownable} from "/Users/jd/Desktop/work/FLBlockchain/integration/Ownable.sol";

contract SimpleCoordinator is Ownable(msg.sender) {
    event UpdateSubmitted(address indexed _trainer, uint256 indexed _numDatapoints, uint256 indexed _reward);
    uint256 public incentivePerDatapoint;
    uint16 public numberUpdatesRequested;
    uint256 public maxDataPoints;

    constructor(uint256 _incentiveInWei, uint16 _numberUpdatesRequested, uint256 _maxDataPoints) payable {
        setIncentive(_incentiveInWei);
        numberUpdatesRequested = _numberUpdatesRequested;
        maxDataPoints = _maxDataPoints;
        // Ensure contract has enough balance for maximum number of data points requested
        // require(msg.value >= (incentivePerDatapoint * (maxDataPoints)), "Not enough deposit");
        
    }

    function setIncentive(uint256 _incentiveInWei) public onlyOwner {
        incentivePerDatapoint = _incentiveInWei;
    }
    function submitUpdate(uint256 _numDatapoints) public payable {
        uint256 reward = (_numDatapoints * (incentivePerDatapoint)) / (numberUpdatesRequested);
        // require(address(this).balance >= reward, "Not enough balance");
        payable(msg.sender).transfer(reward);
        emit UpdateSubmitted(msg.sender, _numDatapoints, reward);
    }

    function distributeIncentive(address _trainer) private {

    }
}