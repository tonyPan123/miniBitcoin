# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 20:22:12 2023

@author: panji
"""

import threading
import json
import time
from hashlib import sha256 as H
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from hashlib import sha256 as H
from nacl.signing import SigningKey
import numpy as np
from random import randint

class Bad_Node: 
    def __init__(self,channels,pool,event,blockchains):
        
        self.channels = channels
        self.pool = pool
        self.event = event
        self.blockchains = blockchains
    def run(self):
        threading.Thread(target=self.do_bad).start() 
        
    def do_bad(self):
        while True:
            if self.event.is_set():
                break
            transaction = self.pool.get()
            self.pool.put(transaction)
        
            block={}
            nonce = 0
            front_string=str(transaction)
            #Bad prev or missing fields or fake nonce
            seed = np.random.random(1)[0]
            if seed < 0.33:
                block= {"tx":transaction, "prev":H(b"bad").hexdigest()}
                front_string = front_string + block["prev"]
            elif seed < 0.67: 
                block= {"tx":transaction}
            else:  
                block= {"tx":transaction, "prev":H(bytes(str(self.blockchains[randint(0, 7)][-1:][0]),'utf-8')).hexdigest()}
                nonce=25
                target = front_string+block["prev"]+hex(nonce)
                hash_value = H(bytes(str(target),'utf-8')).hexdigest() 
                block={**block, "nonce":hex(nonce), "pow":hash_value} 
                for i in range(len(self.channels)):
                    self.channels[i].put(block)
                time.sleep(0.05)
                continue

            while True:
                target = front_string + hex(nonce)
                hash_value = H(bytes(str(target),'utf-8')).hexdigest() 
                if int(hash_value,16) <= 0x07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:
                   block={**block, "nonce":hex(nonce), "pow":hash_value} 
                   #print("Bad coming")
                   for i in range(len(self.channels)):
                       self.channels[i].put(block)
                   break    
                nonce = nonce+1


            time.sleep(0.05)
                    
                    
                    
                    
                    
                    
                    