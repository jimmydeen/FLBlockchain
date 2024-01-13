// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
using SafeMath for int16;
using SafeMath for int256;

contract SimpleCoordinator is Ownable {

    int256 public incentivePerDatapoint;
    int16 public numberUpdatesRequested;
    int256 public maxDataPoints;

    constructor(int256 _incentive, int16 _numberUpdatesRequested, int256 _maxDataPoints) payable {
        setIncentive(_incentive);
        numberUpdatesRequested = _numberUpdatesRequested;
        maxDataPoints = _maxDataPoints;
        // Ensure contract has enough balance for maximum number of data points requested
        require(msg.value >= (incentivePerDatapoint.mul(maxDataPoints)), "Not enough deposit");

    }

    function setIncentive(int256 _incentive) public onlyOwner {
        incentivePerDatapoint = _incentive;
    }
    function submitUpdate(int256 _numDatapoints) public payable {
        int256 reward = (_numDatapoints.mul(incentivePerDatapoint)).div(numberUpdatesRequested);
        require(address(this).balance >= reward, "Not enough balance");
        payable(msg.sender).transfer(reward);
    }

    function distributeIncentive(address _trainer) {

    }
}