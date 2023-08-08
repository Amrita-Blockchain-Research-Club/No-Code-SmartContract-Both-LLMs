pragma solidity ^0.8.0;

contract TransactionsMonitoringSystem {

    // Events

    event TransactionCreated(
        uint256 indexed transactionId,
        address sender,
        address recipient,
        uint256 amount
    );

    // Structs

    struct Transaction {
        uint256 id;
        address sender;
        address recipient;
        uint256 amount;
    }

    // State variables

    mapping(uint256 => Transaction) private transactions;
    uint256 private nextTransactionId = 1;

    // Functions

    /**
     * Creates a new transaction.
     *
     * @param sender The address of the sender.
     * @param recipient The address of the recipient.
     * @param amount The amount of the transaction.
     */
    function createTransaction(
        address sender,
        address recipient,
        uint256 amount
    ) public {
        // Create a new transaction.
        Transaction memory transaction = Transaction(
            nextTransactionId,
            sender,
            recipient,
            amount
        );

        // Store the transaction in the state.
        transactions[nextTransactionId] = transaction;

        // Increment the next transaction ID.
        nextTransactionId++;

        // Emit a transaction created event.
        emit TransactionCreated(
            transaction.id,
            transaction.sender,
            transaction.recipient,
            transaction.amount
        );
    }

    /**
     * Gets a transaction by its ID.
     *
     * @param transactionId The ID of the transaction.
     * @return The transaction, or null if it does not exist.
     */
    function getTransaction(uint256 transactionId) public view returns (Transaction) {
        return transactions[transactionId];
    }

    /**
     * Gets all transactions.
     *
     * @return An array of all transactions.
     */
    function getAllTransactions() public view returns (Transaction[] memory) {
        // Get all transaction IDs.
        uint256[] memory transactionIds = new uint256[](transactions.length);
        for (uint256 i = 0; i < transactions.length; i++) {
            transactionIds[i] = transactions[i].id;
        }

        // Sort the transaction IDs.
        sort(transactionIds);

        // Get all transactions.
        Transaction[] memory transactions = new Transaction[](transactionIds.length);
        for (uint256 i = 0; i < transactionIds.length; i++) {
            transactions[i] = transactions[transactionIds[i]];
        }

        return transactions;
    }
}