from flask import Flask, request, jsonify, render_template
import hashlib
import time
import json

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1,
                          timestamp=time.time(),
                          data=data,
                          previous_hash=last_block.hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        while not block.hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()

@app.route('/')
def index():
    return render_template("index.html")  # Ensure index.html is in the templates folder

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json['data']
    blockchain.add_block(data)
    return jsonify(blockchain.get_last_block().__dict__)

@app.route('/get_blockchain', methods=['GET'])
def get_blockchain():
    return jsonify([block.__dict__ for block in blockchain.chain])

if __name__ == "__main__":
    blockchain = Blockchain()
    app.run(debug=True)
