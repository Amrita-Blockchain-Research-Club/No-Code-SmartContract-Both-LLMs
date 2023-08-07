pragma solidity ^0.8.0;

contract Add16 {
    // The 16 numbers to be added
    uint256[] private numbers;

    // The total sum of the 16 numbers
    uint256 private sum;

    // Event emitted when the numbers are added
    event NumbersAdded(uint256[] numbers, uint256 sum);

    // Constructor that sets the 16 numbers to be added
    constructor(uint256[] memory numbers) {
        this.numbers = numbers;
    }

    // Function to add the 16 numbers and emit an event
    function addNumbers() public {
        for (uint256 i = 0; i < numbers.length; i++) {
            sum += numbers[i];
        }

        emit NumbersAdded(numbers, sum);
    }

    // Getter function to get the total sum of the 16 numbers
    function getSum() public view returns (uint256) {
        return sum;
    }
}