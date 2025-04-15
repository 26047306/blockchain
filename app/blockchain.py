# blockchain.py
import time
import hashlib
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        last_block = self.chain[-1] if self.chain else None
        new_block = Block(index=(last_block.index + 1 if last_block else 1),
                          timestamp=time.time(),
                          data=data,
                          previous_hash=last_block.hash if last_block else "0")
        self.chain.append(new_block)

    def get_chain(self):
        return [block.__dict__ for block in self.chain]
