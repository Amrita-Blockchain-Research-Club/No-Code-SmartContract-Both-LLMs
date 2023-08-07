pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract VotingSystem {
    using SafeMath for uint256;

    // Events
    event Voted(address voter, uint256 candidateId);

    // Structs
    struct Candidate {
        string name;
        uint256 votes;
    }

    // State variables
    address payable public owner;
    mapping(uint256 => Candidate) public candidates;
    uint256 public openTime;
    uint256 public closeTime;

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    // Constructor
    constructor(uint256 _openTime, uint256 _closeTime) {
        owner = msg.sender;
        openTime = _openTime;
        closeTime = _closeTime;
    }

    // Public functions
    function addCandidate(string memory _name) public onlyOwner {
        candidates[candidates.length] = Candidate(_name, 0);
    }

    function vote(uint256 _candidateId) public {
        require(block.timestamp >= openTime && block.timestamp <= closeTime, "Voting is not open");
        require(ERC20(msg.sender).balanceOf(address(this)) >= 1000000000000000000, "Not enough balance to vote");

        candidates[_candidateId].votes = candidates[_candidateId].votes.add(1);
        ERC20(msg.sender).transfer(address(0), 1000000000000000000);

        emit Voted(msg.sender, _candidateId);
    }

    function getCandidates() public view returns (Candidate[] memory) {
        return candidates;
    }

    function getWinner() public view returns (Candidate memory) {
        uint256 maxVotes = 0;
        uint256 winnerId = 0;

        for (uint256 i = 0; i < candidates.length; i++) {
            if (candidates[i].votes > maxVotes) {
                maxVotes = candidates[i].votes;
                winnerId = i;
            }
        }

        return candidates[winnerId];
    }
}