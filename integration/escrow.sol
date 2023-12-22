// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataEscrow {
    address payable public sender;
    address payable public requester;
    string private dataHash;
    uint256 public paymentAmount;
    bool public isDataSubmitted;
    bool public isPaymentMade;

    event DataSubmitted(string _dataHash);
    event PaymentMade(uint256 _amount);
    event DataReleased(string _dataHash);

    constructor(address payable _sender, address payable _requester) {
        sender = _sender;
        requester = _requester;
    }

    function submitData(string calldata _dataHash) external {
        require(msg.sender == sender, "Only the sender can submit data");
        require(!isDataSubmitted, "Data already submitted");
        dataHash = _dataHash;
        isDataSubmitted = true;
        paymentAmount = calculatePayment(_dataHash);

        emit DataSubmitted(_dataHash);
    }

    function calculatePayment(string memory _dataHash) private pure returns (uint256) {
        // Simplified payment calculation based on data hash
        // In a real-world scenario, this would be more complex
        return uint256(keccak256(abi.encodePacked(_dataHash))) % 100 ether;
    }

    function makePayment() external payable {
        require(msg.sender == requester, "Only the requester can make payment");
        require(isDataSubmitted, "Data not yet submitted");
        require(msg.value == paymentAmount, "Incorrect payment amount");
        require(!isPaymentMade, "Payment already made");

        isPaymentMade = true;
        sender.transfer(msg.value);

        emit PaymentMade(msg.value);
    }

    function getData() external view returns (string memory) {
        require(msg.sender == requester, "Only the requester can access data");
        require(isPaymentMade, "Payment not made");

        return dataHash;
    }
}
