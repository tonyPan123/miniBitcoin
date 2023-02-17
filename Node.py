# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 15:25:40 2023

@author: panji
"""
import threading
import json
import time
from hashlib import sha256 as H
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder

class Node: 

    
    def __init__(self, initial_list, index, pool, event, lock, channels):
        self.index = index
        self.pool = pool
        self.blockchains = initial_list
        self.event = event
        self.netlock = lock
        self.channels = channels
        self.failverified = set()
        self.node_lock = threading.Lock()
    def run(self):
        threading.Thread(target=self.mining_blocks).start()   
        threading.Thread(target=self.check_broadcasting).start()  
        
    def mining_blocks(self):
        while True:
            if self.event.is_set():
                break
            transaction=[]
            try:
                transaction = self.pool.get()
            except:
                print("No transaction left")
                time.sleep(1)
                continue
            if transaction["number"] in self.failverified:
            #    self.pool.put(transaction)
            #    time.sleep(1)
                continue
            #print("start!")
            self.pool.put(transaction)
            self.node_lock.acquire()
            #if (self.verify_transaction(self.blockchains[self.index],len(self.blockchains[self.index]),transaction) == False):
                #self.failverified.add(transaction["number"])
            #    self.pool.put(transaction)
            #    self.node_lock.release()
            #    time.sleep(1)
            #    continue
            block= {"tx":transaction, "prev":H(bytes(str(self.blockchains[self.index][-1:][0]),'utf-8')).hexdigest()}
            self.node_lock.release()
            #print(transaction["number"])
            nonce = 0
            front_string = str(block['tx']) + block['prev']
            while True:
                target = front_string + hex(nonce)
                hash_value = H(bytes(str(target),'utf-8')).hexdigest() 
                
                # Find the correct nonce
                if int(hash_value,16) <= 0x07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:
                    self.node_lock.acquire()
                    
                    block={**block, "nonce":hex(nonce), "pow":hash_value} 
                    #Verify whole block?
                    if (self.verify_block(self.blockchains[self.index],len(self.blockchains[self.index]),block) == False):
                        #print("False?")
                        self.node_lock.release()
                        #self.failverified.add(transaction["number"])
                        
                        break
                    # Whenever successfully add a new element, give blocks failed to verfied one more chance
                    #self.failverified=set()
                    
                    self.netlock.acquire()
                    self.blockchains[self.index].append(block)
                    #Broadcast the block
                    for i in range(len(self.channels)):
                        if i != self.index:
                            self.channels[i].put(block)
                    self.netlock.release()
                    self.node_lock.release()
                    break
                nonce=nonce+1
            #time.sleep(1)
 
    # Worker for check broadcasting
    def check_broadcasting(self):
        while True:
            if self.event.is_set():
                break
            if self.channels[self.index].empty() == False:
                block = self.channels[self.index].get()
                self.node_lock.acquire()
                #Check block validity
                if self.verify_block(self.blockchains[self.index],len(self.blockchains[self.index]),block):
                    print("Accepting Broadcasting at Node"+str(self.index)+"\n") 
                    self.netlock.acquire()
                    self.blockchains[self.index].append(block)
                    self.netlock.release()
                else:
                    self.check_conflicts()
                    #print(block["tx"])
                self.node_lock.release()
            
            #time.sleep(2)
                

    # Rountine for checking conflicts(forking)    
    def check_conflicts(self):  
        length=len(self.blockchains[self.index])
        max_length = length
        max_index = self.index
        max_blockchain = []
        for i in range(8):
            if i==self.index:
                continue
            #Simulate network environment to copy as a whole
            self.netlock.acquire()
            blockchain=self.blockchains[i].copy()
            self.netlock.release()
            #TODO: add support for marking some nodes as intrust
            if self.verify_chains(blockchain) and len(blockchain) > max_length:
                max_length = len(blockchain)
                max_index = i
                max_blockchain = blockchain
        if max_index != self.index:     
            self.check_fork(max_blockchain)
            #self.blockchains[self.index].append(max_blockchain[length])
            #print("Accepting Broadcasting at Node"+str(self.index)+"\n")    
     
    # SubRountine that check forking    
    def check_fork(self, gindex):
        for i in range(len(self.blockchains[self.index])):
            if (self.blockchains[self.index][i] != gindex[i]):
                print("Find Forking at"+str(self.index)+", fixing...\n") 
                #print(self.blockchains[self.index])
                #for j in range(len(self.blockchains[self.index])-i):
                #    self.pool.put(self.blockchains[self.index].pop()["tx"])
                self.netlock.acquire()    
                self.blockchains[self.index] = gindex
                self.netlock.release()   
      
    # Validate a whole blockchain
    def verify_chains(self,blockchain):
        for i in range(1,len(blockchain)):
            if self.verify_block(blockchain,i,blockchain[i]) == False:
                return False
        return True
        
    # Validate a block in the context of a blockchain
    # Assume index >= 1    
    # Block is the one at index or to be added to the specificied index
    def verify_block(self,blockchain,index,block):
        for attrib in ["tx", "prev", "nonce", "pow"]:
            if block.get(item, None) is None:
                print("missing block attributes")
                return False
        if self.verify_transaction(blockchain,index,block["tx"]) == False:
            return False
        prev = H(bytes(str(blockchain[index-1]),'utf-8')).hexdigest()
        if prev != block["prev"]:
            print("Prev hash in block is wrong\n")
            return False
        target = str(block['tx']) + block['prev'] + block['nonce']
        hash_value = H(bytes(str(target),'utf-8')).hexdigest() 
        if hash_value != block["pow"] or int(hash_value,16) >  0x07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:  
            print("Nonce is invalid!\n")
            return False
        return True
 
    
     
    #Verifying a block, containing verifying a transaction
    def verify_transaction(self,blockchain,index,transaction):
        #Check for sign, equal in, equal out, and number(result of hash)
        if transaction.get("input", None) is None or len(transaction["input"]) == 0:
          print("invalid transaction format")
          return False
        if transaction.get("output", None) is None or transaction.get("sig", None) is None \
           or transaction.get("number", None) is None:
          print("invalid transaction format")
          return False
        publicKey = transaction["input"][0]["output"]["pubkey"]
        verify_key = VerifyKey(bytes.fromhex(publicKey), encoder=HexEncoder)
        text = {"input":transaction["input"], "output":transaction["output"]}
        signature_bytes = bytes.fromhex(transaction["sig"])
        try:
            verify_key.verify(bytes(str(text),'utf-8'),signature_bytes)
        except:
            print("signature is bad\n")
            return False
        text = {**text,**{"sig": transaction["sig"]}}
        number = H(bytes(str(text),'utf-8')).hexdigest()
        if number != transaction["number"]:
            print("Transaction number is bad\n")
            return False
        
        # Check for input equal output
        # total_input=0
        # total_output=0
        # for coin_input in transaction["input"]:
        #     total_input=total_input+coin_input["output"]["value"]
        total_input = sum([coin_input["output"]["value"] for coin_input in transaction["input"]])
        # for coin_output in transaction["output"]:
        #     total_output=total_output+coin_output["value"]
        total_output = sum([coin_output["value"] for coin_output in transaction["output"]])
        
        if total_input != total_output:
            print("Input is not equal to output in the transaction")
            return False
        
        
        #Check for input existence and double spend
        for coin_input in transaction["input"]:
            if coin_input["output"].get("value", None) is None or coin_input["output"].get("pubkey", None) is None:
                print("invalid transaction output format")
                return False
            flag = False
            for i in range(index):
                iter_transaction = blockchain[i]["tx"]
                # Check double spend here
                if flag == True:
                    for iter_input in iter_transaction["input"]:
                        if iter_input["number"] == coin_input["number"]:
                            if iter_input["output"]["value"] == coin_input["output"]["value"] and iter_input["output"]["pubkey"] == coin_input["output"]["pubkey"]:
                                print("Double Spend!\n")
                                #print(transaction["number"])
                                return False                
                if iter_transaction["number"] == coin_input["number"]:
                    for iter_output in iter_transaction["output"]:
                        if iter_output["value"] == coin_input["output"]["value"] and iter_output["pubkey"] == coin_input["output"]["pubkey"]:
                            flag = True

                
            #Fail to find the output corresponding to the input    
            if flag == False:
                return False 
        return True





