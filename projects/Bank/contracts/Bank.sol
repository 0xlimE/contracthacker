pragma solidity ^0.6.0;

contract Bank{
  address private _owner;
    constructor() public payable{
        _owner = msg.sender;
    }
   mapping(address=>uint) public customerBalance;

   function getBalance(address customer) public view returns (uint balance) {
     return customerBalance[customer];
   }
   
   function deposit() public payable {
     customerBalance[msg.sender] = customerBalance[msg.sender]+= msg.value;
   }

   function withdraw() public payable {
     uint balance = customerBalance[msg.sender];
     if(balance == 0){
         revert();
     }
     msg.sender.call{value:balance}("");
     customerBalance[msg.sender] = 0;
   }
}
