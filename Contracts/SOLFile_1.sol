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
    mapping(uint256 => Candidate) public candidates;
    uint256 public totalVotes;

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner(), "Only the owner can call this function");
        _;
    }

    // Constructor
    constructor(address _owner) {
        owner = _owner;
    }

    // Public functions
    function addCandidate(string memory name) public onlyOwner {
        uint256 candidateId = candidates.length;
        candidates[candidateId] = Candidate(name, 0);
    }

    function vote(uint256 candidateId) public {
        require(candidates[candidateId].name != "", "Candidate does not exist");

        totalVotes = totalVotes.add(1);
        candidates[candidateId].votes = candidates[candidateId].votes.add(1);

        emit Voted(msg.sender, candidateId);
    }

    function getCandidates() public view returns (Candidate[] memory) {
        uint256 length = candidates.length;
        Candidate[] memory candidatesArray = new Candidate[](length);

        for (uint256 i = 0; i < length; i++) {
            candidatesArray[i] = candidates[i];
        }

        return candidatesArray;
    }

    function getCandidate(uint256 candidateId) public view returns (Candidate memory) {
        return candidates[candidateId];
    }

    function getTotalVotes() public view returns (uint256) {
        return totalVotes;
    }

    // Private variables
    address private owner;
}