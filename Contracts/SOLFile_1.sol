pragma solidity ^0.8.0;

contract Voting {

    // The address of the account that can call the `vote` function.
    address public owner;

    // The list of candidates in the election.
    string[] public candidates;

    // The mapping from each candidate's address to the number of votes they have received.
    mapping(address => uint256) public votes;

    // The constructor sets the `owner` address to the address that deployed the contract.
    constructor() {
        owner = msg.sender;
    }

    // The `addCandidate` function allows the owner to add a candidate to the election.
    function addCandidate(string memory candidate) public onlyOwner {
        candidates.push(candidate);
    }

    // The `vote` function allows a voter to cast a vote for a candidate.
    function vote(string memory candidate) public {
        // Check that the voter is not the owner of the contract.
        require(msg.sender != owner);

        // Check that the candidate is a valid candidate.
        require(candidates.indexOf(candidate) != -1);

        // Increment the number of votes for the candidate.
        votes[address(this)]++;
    }

    // The `getWinner` function returns the address of the candidate with the most votes.
    function getWinner() public view returns (address) {
        uint256 maxVotes = 0;
        address winner = address(0);

        for (uint256 i = 0; i < candidates.length; i++) {
            uint256 votesForCandidate = votes[address(this)];

            if (votesForCandidate > maxVotes) {
                maxVotes = votesForCandidate;
                winner = address(this);
            }
        }

        return winner;
    }
}