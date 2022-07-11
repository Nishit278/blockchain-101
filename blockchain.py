import datetime #timestamp for block
import hashlib  #hashing 
import json #encode blocks before hashing
from flask import Flask, jsonify

# Building a blockchain
class Blockchain:
    def __init__(self):
        self.chain = [] #list of blocks in blockchain 
        self.create_block(proof = 1, previous_hash = "0") #creating the genesis block
    
    def create_block(self, proof, previous_hash):
        block = {"index": len(self.chain)+1,
                 "timestamp": str(datetime.datetime.now()),
                 "proof": proof,
                 "previous_hash": previous_hash,
                }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # hash_operation = hashlib.sha256(str(new_proof - previous_proof).encode()).hexdigest()
            if hash_operation[:5] == "00000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # Check if the block is valid by checking the previous_hash and proof
    # The previous_hash is the hash of the previous block
    # The proof is the proof of work which is set according to the difficulty
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode() #dumps() takes an object and makes string out of it, sort_keys = True sorts the keys of the object, sha256 needs an encoded string thats why we encode it
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block): #if the previous_hash of the block is not the hash of the previous block, the chain is not valid
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            # hash_operation = hashlib.sha256(str(proof - previous_proof).encode()).hexdigest()
            if hash_operation[:5] != "00000":
                return False
            previous_block = block
            block_index += 1
        return True

# Mining our Blockchain
# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route("/mine_block", methods = ["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof) # method to find the proof of the current block, proof is similar to nonce.
    previous_hash = blockchain.hash(previous_block) # method to hash the previous block
    block = blockchain.create_block(proof, previous_hash) # method to create a new block with the proof and previous_hash
    response = {"message": "Congratulations, you just mined a block!",
                "index": block["index"],
                "timestamp": block["timestamp"],
                "proof": block["proof"],
                "previous_hash": block["previous_hash"],
                }
    return jsonify(response), 200

# Getting the full Blockchain
@app.route("/get_chain", methods = ["GET"])
def get_chain():
    response = {"chain": blockchain.chain,
                "length": len(blockchain.chain),
                }
    return jsonify(response), 200

# Running the app
app.run(host = "0.0.0.0" , port = 5000)