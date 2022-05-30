pragma solidity 0.7.4;

contract Charity {
    address private _owner;

    constructor() public payable {
        _owner = msg.sender;
    }

    mapping(address => uint256) public donatorBalance;
    mapping(address => uint256) public charityBalance;
    mapping(address => bool) public donatedToContract;

    function getDonatorBalance(address donator) public view returns (uint256 balance){
        return donatorBalance[donator];
    }

    function getCharityBalance(address charity) public view returns (uint256 balance){
        return charityBalance[charity];
    }

    function deposit() public payable {
        donatorBalance[msg.sender] = donatorBalance[msg.sender] += msg.value;
    }

    function donate(uint256 amount, address charity) public payable {
        require(amount <= donatorBalance[msg.sender], "Insufficient balance");
        require(
            charity != address(this),
            "Use donateToContract() function to donate to us!"
        );
        donatorBalance[msg.sender] -= amount;
        charityBalance[charity] += amount;
        msg.sender.call{value: 0}("Thanks for your donation.");
    }

    function donateToContract(uint256 amount) public payable {
        require(amount <= donatorBalance[msg.sender], "Insufficient balance");
        require(
            !donatedToContract[msg.sender],
            "Can only donate to contract once!"
        );
        donatedToContract[msg.sender] = true;
        charityBalance[address(this)] += amount;
        msg.sender.call{value: 0}("Thanks for your donation.");
        donatorBalance[msg.sender] -= amount;
    }

    function withdraw() public payable {
        uint256 balance = donatorBalance[msg.sender];
        if (balance == 0) {
            revert();
        }
        if (address(this).balance < balance) {
            //Something bad happened, and we have paid out more than we should, we need to refund the donator the max we can.
            balance = address(this).balance;
        }
        //NO REENTRANCY!!
        donatorBalance[msg.sender] = 0;
        payable(msg.sender).transfer(balance);
    }

    function payCharity(address charity) public payable {
        require(msg.sender == _owner, "Only the contract owner can do this");
        uint256 balance = charityBalance[charity];
        if (balance == 0) {
            revert();
        }
        //NO REENTRANCY!!
        charityBalance[msg.sender] = 0;
        payable(charity).transfer(balance);
    }
}
