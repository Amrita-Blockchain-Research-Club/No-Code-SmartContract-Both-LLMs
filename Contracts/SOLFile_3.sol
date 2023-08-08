pragma solidity ^0.8.0;

contract HelloWorld {
  string public message = "Hello, World!";

  function getMessage() public view returns (string) {
    return message;
  }
}