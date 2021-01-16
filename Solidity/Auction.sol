pragma solidity ^0.5.0;

contract Auction {
    address payable private farmer;
    
    event HighestBidIncreased(address bidder, uint amount); //Stores the transaction logs they can be obtained using emit
    event AuctionEnded(address winner, uint amount);
    
    bool end = false;
    
    uint public highestPrice;
    address payable public highestBidder;
    
    
    modifier notOwner(){
        require(msg.sender != farmer);
        _;
    }
    
    modifier onlyOwner(){
        require(
            msg.sender == farmer,
            "You are not the owner.");
        _;
    }
    
    constructor(
        address payable _farmer) public {
            farmer = _farmer;
        }
        
    
    function placeBid() notOwner public payable {
        require(end == false,
                "This auction has already ended and you cannot place anymore bids");
        require(msg.value > highestPrice,
                "Bid needs to be higher than previous Bid");
        if(highestPrice != 0) {
            highestBidder.transfer(highestPrice);
        }
        
        highestBidder = msg.sender;
        highestPrice = msg.value;
        emit HighestBidIncreased(msg.sender, msg.value);

    }
    
    function auctionEnd() onlyOwner public {
        end = true;
        emit AuctionEnded(highestBidder, highestPrice); //We use emit to access all the details of the transaction.
        farmer.transfer(highestPrice);
    }
    
}

