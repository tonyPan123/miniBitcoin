# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 12:05:46 2023

@author: panji
"""

import threading
import queue
from threading import Event
import numpy as np
import nacl.utils
from hashlib import sha256 as H
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
import sys, traceback
import json
import time

from Node import Node

class Driver:
    # Global Data Structure
    txs_list=[]
    pool=queue.Queue()
    blockchains=[]
    
    def crafting_transactions(self):
        # Creating Transactions
        # Prepare public/private keys
        
        skalice = SigningKey.generate()
        pkalice = skalice.verify_key
        skbob = SigningKey.generate()
        pkbob = skbob.verify_key
        skcarol = SigningKey.generate()
        pkcarol = skcarol.verify_key
        sk4 = SigningKey.generate()
        pk4 = sk4.verify_key
        sk5 = SigningKey.generate()
        pk5 = sk5.verify_key
        sk6 = SigningKey.generate()
        pk6 = sk6.verify_key
        sk7 = SigningKey.generate()
        pk7 = sk7.verify_key
        sk8 = SigningKey.generate()
        pk8 = sk8.verify_key
        
        # Input and output list
        coin_input0 = []
        coin_output0 = [{"value": 100, "pubkey": pkalice.encode(encoder=HexEncoder).hex()}]
        transaction0 = {'input':coin_input0, 'output':coin_output0}
        
        signed0 = skalice.sign(bytes(str(transaction0),'utf-8')).signature.hex()
        #print(len(signed0))
        transaction0 = {**transaction0,**{"sig": signed0}}
        
        # Hash to get name
        number0 = H(bytes(str(transaction0),'utf-8')).hexdigest()
        transaction0 = {**{"number": number0},**transaction0}
        self.txs_list.append(transaction0)
        
        #First block
        coin_input1 = []
        coin_input1.append({'number':transaction0['number'],'output':transaction0['output'][0]})
        coin_output1 = [{"value": 50, "pubkey": pkalice.encode(encoder=HexEncoder).hex()},
                        {"value": 50, "pubkey": pkbob.encode(encoder=HexEncoder).hex()}]
    
        transaction1 = {'input':coin_input1, 'output':coin_output1}
        signed1 = skalice.sign(bytes(str(transaction1),'utf-8')).signature.hex()
        #pkalice.verify(bytes(str(transaction1),'utf-8'),bytes.fromhex(signed1))
        transaction1 = {**transaction1,**{"sig": signed1}}
        number1 = H(bytes(str(transaction1),'utf-8')).hexdigest()
        transaction1 = {**{"number": number1},**transaction1}
        
        
        #self.pool.append(transaction1)
        
        #Check for forking
        coin_input6 = []
        coin_input6.append({'number':transaction0['number'],'output':transaction0['output'][0]})
        coin_output6 = [{"value": 75, "pubkey": pkcarol.encode(encoder=HexEncoder).hex()},
                        {"value": 25, "pubkey": pkalice.encode(encoder=HexEncoder).hex()}]
    
        transaction6 = {'input':coin_input6, 'output':coin_output6}
        signed6 = skalice.sign(bytes(str(transaction6),'utf-8')).signature.hex()
        transaction6 = {**transaction6,**{"sig": signed6}}
        number6 = H(bytes(str(transaction6),'utf-8')).hexdigest()
        transaction6 = {**{"number": number6},**transaction6}
        self.txs_list.append(transaction1)
        self.txs_list.append(transaction6)
        #Second block
        coin_input2 = []
        coin_input2.append({'number':transaction1['number'],'output':transaction1['output'][1]})
        coin_output2 = [{"value": 25, "pubkey": pkcarol.encode(encoder=HexEncoder).hex()},
                        {"value": 25, "pubkey": pkalice.encode(encoder=HexEncoder).hex()}]
    
        transaction2 = {'input':coin_input2, 'output':coin_output2}
        signed2 = skbob.sign(bytes(str(transaction2),'utf-8')).signature.hex()
        transaction2 = {**transaction2,**{"sig": signed2}}
        number2 = H(bytes(str(transaction2),'utf-8')).hexdigest()
        transaction2 = {**{"number": number2},**transaction2}
        

        #self.pool.append(transaction2)
        
        #Sixth block: testing for fork
                #Second block

        
        self.txs_list.append(transaction2)
        
        
        
        #Third block
        coin_input3 = []
        coin_input3.append({'number':transaction1['number'],'output':transaction1['output'][0]})
        coin_input3.append({'number':transaction2['number'],'output':transaction2['output'][1]})
        coin_output3 = [{"value": 75, "pubkey": pk4.encode(encoder=HexEncoder).hex()}]
    
        transaction3 = {'input':coin_input3, 'output':coin_output3}
        signed3 = skalice.sign(bytes(str(transaction3),'utf-8')).signature.hex()
        transaction3 = {**transaction3,**{"sig": signed3}}
        number3 = H(bytes(str(transaction3),'utf-8')).hexdigest()
        transaction3 = {**{"number": number3},**transaction3}
        
        self.txs_list.append(transaction3)
        
        
        #Fourth block is a double spend with block 3, also may lead to forking
        coin_input4 = []
        coin_input4.append({'number':transaction1['number'],'output':transaction1['output'][0]})
        coin_input4.append({'number':transaction2['number'],'output':transaction2['output'][1]})
        coin_output4 = [{"value": 75, "pubkey": pk5.encode(encoder=HexEncoder).hex()}]
    
        transaction4 = {'input':coin_input4, 'output':coin_output4}
        signed4 = skalice.sign(bytes(str(transaction4),'utf-8')).signature.hex()
        transaction4 = {**transaction4,**{"sig": signed4}}
        number4 = H(bytes(str(transaction4),'utf-8')).hexdigest()
        transaction4 = {**{"number": number4},**transaction4}
        
        #self.txs_list.append(transaction4)
        
        #Fifth block is same as fourth block
        #self.txs_list.append(transaction4)
        
        #Seventh block is normal(which should lead to the deletion of fork at 6th block if possible)
        coin_input7 = []
        coin_input7.append({'number':transaction3['number'],'output':transaction3['output'][0]})
        coin_output7 = [{"value": 75, "pubkey": pk5.encode(encoder=HexEncoder).hex()}]
    
        transaction7 = {'input':coin_input7, 'output':coin_output7}
        signed7 = sk4.sign(bytes(str(transaction7),'utf-8')).signature.hex()
        transaction7 = {**transaction7,**{"sig": signed7}}
        number7 = H(bytes(str(transaction7),'utf-8')).hexdigest()
        transaction7 = {**{"number": number7},**transaction7}
        
        self.txs_list.append(transaction7)        
        
        coin_input8 = []
        coin_input8.append({'number':transaction7['number'],'output':transaction7['output'][0]})
        coin_output8 = [{"value": 25, "pubkey": pk6.encode(encoder=HexEncoder).hex()},
                        {"value": 25, "pubkey": pk7.encode(encoder=HexEncoder).hex()},
                        {"value": 25, "pubkey": pk8.encode(encoder=HexEncoder).hex()}]
    
        transaction8 = {'input':coin_input8, 'output':coin_output8}
        signed8 = sk5.sign(bytes(str(transaction8),'utf-8')).signature.hex()
        transaction8 = {**transaction8,**{"sig": signed8}}
        number8 = H(bytes(str(transaction8),'utf-8')).hexdigest()
        transaction8 = {**{"number": number8},**transaction8}
        
        self.txs_list.append(transaction8)    
        
        coin_input9 = []
        coin_input9.append({'number':transaction2['number'],'output':transaction2['output'][0]})
        coin_output9 = [{"value": 25, "pubkey": pk5.encode(encoder=HexEncoder).hex()}]
    
        transaction9 = {'input':coin_input9, 'output':coin_output9}
        signed9 = skcarol.sign(bytes(str(transaction9),'utf-8')).signature.hex()
        transaction9 = {**transaction9,**{"sig": signed9}}
        number9 = H(bytes(str(transaction9),'utf-8')).hexdigest()
        transaction9 = {**{"number": number9},**transaction9}
        
        self.txs_list.append(transaction9) 
        
        
        

        with open("transactions.json", "w") as outfile:
            json.dump(self.txs_list, outfile, indent=2)
            
            
            
    def main(self):
        #Read the transactions
        self.crafting_transactions()
        
        transactions = []    
        with open('transactions.json', 'r') as infile: 
            transactions = json.loads(infile.read())
            
            
        #make genesis block
        block0= {"tx":transactions[0], "prev":12345, "nonce":12345, "pow":12345}    
        blockchains = [[block0] for i in range(8)] 
        channels = [queue.Queue() for i in range(8)]
        
        event = Event()
        nodes_num=8
        #Lock for coordination
        lock = threading.Lock()
        for i in range(nodes_num):
            Node(blockchains,i,self.pool,event,lock,channels).run()
            
        # Add to pool in 1s period  
        for i in range(len(transactions)-1):
            time.sleep(np.random.random(1)[0])
            self.pool.put(transactions[(i+1)])
            
        time.sleep(30)  
        print("Stopping!")
        #for thread_id, frame in sys._current_frames().items():
        #    print('Stack for thread {}'.format(thread_id))
        #    traceback.print_stack(frame)
        #    print('')
        event.set()
        for i in range(nodes_num):  
            with open("block_chain_"+str(i)+".json", "w") as outfile:
                json.dump(blockchains[i], outfile, indent=2)   
            
    #def initialize_transaction(self,)            
            
        
if __name__ == "__main__":
	(Driver()).main()  