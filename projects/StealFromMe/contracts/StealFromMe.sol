pragma solidity ^0.6.0;

 
contract StealFromMe {
    address private _owner;
    constructor() public payable{
        _owner = msg.sender;
    }

    function steal() public payable {
        msg.sender.transfer(address(this).balance);
    }
}