import hashlib
import json
from time import time
#! Only need this library to see size of dictionary
#! Remove when not required
from sys import getsizeof

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    #? Should all pending transactions get added to the new block?
    #! Bitcoin has a limit of 990000 bytes
    #! When experimenting here each transaction was 232B
    # Implementing a limit of about 1KB i.e. 4 transactions

    def add_block(self):
        if len(self.chain) == 0:
            previous_hash = self.hash("The first hash starts here".encode())
        else:
            previous_hash = self.prev_block()['curr_hash']
        flag = 0
        if len(self.pending_transactions) > 4:
            flag = 1
        transaction_hash = self.transaction_hash(flag)
        # Need to store time so that the timestamp is consistent in the find_nonce function
        # and in the parameter in our block
        curr_time = time()
        proof, curr_hash = self.find_nonce(len(self.chain) + 1, curr_time, transaction_hash, 3)
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : curr_time,
            'transactions' : self.pending_transactions[:min(4, len(self.pending_transactions))],
            'proof' : proof,
            'curr_hash' : curr_hash,
            'previous_hash' : previous_hash
        }
        # Pending transactions added to the block
        if flag == 0:
            self.pending_transactions = []
        else:
            del self.pending_transactions[:4]
        self.chain.append(block)
        return block

# TODO Allow the nonce to be a string
#! String.ascii_lowercase and string.digits
    def find_nonce(self, index, timestamp, transaction_hash, difficulty):
        nonce = 0
        mystring = str(index) + str(timestamp) + str(transaction_hash)
        # Increment nonce till the first {difficulty} characters of the
        # hash are 0
        while True:
            possible_hash = self.hash((mystring + str(nonce)).encode())
            if possible_hash[:difficulty] == '0'*difficulty:
                break
            nonce += 1 
        return nonce, possible_hash

    #flag = 0 implies less than 4 pending transactions and thus they can all be added
    def transaction_hash(self, flag):
        if flag == 0:
            transactions = self.pending_transactions
        else:
            transactions = self.pending_transactions[:4]
        i = 0
        hashes = []
        # Combining 2 transactions at a time and then hashing the concatenated string
        # If there are odd number of pending transactions, last string gets hashed as is
        while i < len(transactions):
            if i + 1 < len(transactions):
                tohash = json.dumps(transactions[i], sort_keys = True).encode()
                tohash += json.dumps(transactions[i+1], sort_keys = True).encode()
                hashes.append(self.hash(tohash))
                i += 2
            else:
                hashes.append(self.hash(json.dumps(transactions[i], sort_keys = True).encode()))
                i += 1
        #? Maybe these need to be combined 2 at a time and then hashed, recursively.
        # TODO Look into transaction hash implementations
        transaction_hash = ''.join(hashes)
        transaction_hash = transaction_hash.encode()
        transaction_hash = self.hash(transaction_hash)
        return transaction_hash

    def prev_block(self):
        return self.chain[-1]

    def new_transaction(self,  sender, receiver, amount):
        transaction = {
            'sender' : sender,
            'receiver' : receiver,
            'amount' : amount
        }
        #print(getsizeof(transaction))
        self.pending_transactions.append(transaction)
        return 0

    def hash(self, string):
        temp_hash = hashlib.sha256(string)
        hex_hash = temp_hash.hexdigest()
        return hex_hash

    #Balance is received - sent but pending 'sent' transactions hit the balance too
    #Last 3 elements of the amount parameter in a transaction are ' PP'
    def get_balance(self, user):
        balance = 0
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == user:
                    balance -= float(transaction['amount'][:-3])
                elif transaction['receiver'] == user:
                    balance += float(transaction['amount'][:-3])
        for pending_transaction in self.pending_transactions:
            if pending_transaction['sender'] == user:
                balance -= float(pending_transaction['amount'][:-3])
        return balance

blockchain = Blockchain()
t1 = blockchain.new_transaction('A', 'B', '3 PP')
t2 = blockchain.new_transaction('B', 'C', '1 PP')
t3 = blockchain.new_transaction('A', 'C', '7 PP')
t4 = blockchain.new_transaction('D', 'E', '2 PP')
t5 = blockchain.new_transaction('E', 'F', '4 PP')
block = blockchain.add_block()
block = json.dumps(block, indent=2)
print(block)
block = blockchain.add_block()
block = json.dumps(block, indent=2)
print(block)
print(blockchain.get_balance('B'))

