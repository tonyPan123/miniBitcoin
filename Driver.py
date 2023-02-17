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
from Bad_Node import Bad_Node

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
        
        self.txs_list.append(transaction4)
        
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
        
        coin_input10 = []
        coin_input10.append({'number':transaction8['number'],'output':transaction8['output'][0]})
        coin_output10 = [{"value": 25, "pubkey": pk8.encode(encoder=HexEncoder).hex()}]
    
        transaction10 = {'input':coin_input10, 'output':coin_output10}
        signed10 = sk6.sign(bytes(str(transaction10),'utf-8')).signature.hex()
        transaction10 = {**transaction10,**{"sig": signed10}}
        number10 = H(bytes(str(transaction10),'utf-8')).hexdigest()
        transaction10 = {**{"number": number10},**transaction10}
        
        self.txs_list.append(transaction10) 
        
        coin_input11 = []
        coin_input11.append({'number':transaction8['number'],'output':transaction8['output'][1]})
        coin_output11 = [{"value": 25, "pubkey": pk8.encode(encoder=HexEncoder).hex()}]
    
        transaction11 = {'input':coin_input11, 'output':coin_output11}
        signed11 = sk7.sign(bytes(str(transaction11),'utf-8')).signature.hex()
        transaction11 = {**transaction11,**{"sig": signed11}}
        number11 = H(bytes(str(transaction11),'utf-8')).hexdigest()
        transaction11 = {**{"number": number11},**transaction11}
        
        self.txs_list.append(transaction11) 
        
        coin_input12 = []
        coin_input12.append({'number':transaction8['number'],'output':transaction8['output'][2]})
        coin_input12.append({'number':transaction10['number'],'output':transaction10['output'][0]})
        coin_input12.append({'number':transaction11['number'],'output':transaction11['output'][0]})
        coin_output12 = [{"value": 35, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 40, "pubkey": pkalice.encode(encoder=HexEncoder).hex()}]
    
        transaction12 = {'input':coin_input12, 'output':coin_output12}
        signed12 = sk8.sign(bytes(str(transaction12),'utf-8')).signature.hex()
        transaction12 = {**transaction12,**{"sig": signed12}}
        number12 = H(bytes(str(transaction12),'utf-8')).hexdigest()
        transaction12 = {**{"number": number12},**transaction12}
        
        self.txs_list.append(transaction12) 
        
        coin_input13 = []
        coin_input13.append({'number':transaction12['number'],'output':transaction12['output'][0]})
        coin_input13.append({'number':transaction9['number'],'output':transaction9['output'][0]})
        coin_output13 = [{"value": 60, "pubkey": pkbob.encode(encoder=HexEncoder).hex()}]
    
        transaction13 = {'input':coin_input13, 'output':coin_output13}
        signed13 = sk5.sign(bytes(str(transaction13),'utf-8')).signature.hex()
        transaction13 = {**transaction13,**{"sig": signed13}}
        number13 = H(bytes(str(transaction13),'utf-8')).hexdigest()
        transaction13 = {**{"number": number13},**transaction13}
        
        self.txs_list.append(transaction13) 
        
        coin_input14 = []
        coin_input14.append({'number':transaction13['number'],'output':transaction13['output'][0]})
        coin_output14 = [{"value": 60, "pubkey": pkalice.encode(encoder=HexEncoder).hex()}]
    
        transaction14 = {'input':coin_input14, 'output':coin_output14}
        signed14 = skbob.sign(bytes(str(transaction14),'utf-8')).signature.hex()
        transaction14 = {**transaction14,**{"sig": signed14}}
        number14 = H(bytes(str(transaction14),'utf-8')).hexdigest()
        transaction14 = {**{"number": number14},**transaction14}
        
        self.txs_list.append(transaction14) 
        
        coin_input15 = []
        coin_input15.append({'number':transaction14['number'],'output':transaction14['output'][0]})
        coin_input15.append({'number':transaction12['number'],'output':transaction12['output'][1]})
        coin_output15 = [{"value": 100, "pubkey": pkcarol.encode(encoder=HexEncoder).hex()}]
    
        transaction15 = {'input':coin_input15, 'output':coin_output15}
        signed15 = skalice.sign(bytes(str(transaction15),'utf-8')).signature.hex()
        transaction15 = {**transaction15,**{"sig": signed15}}
        number15 = H(bytes(str(transaction15),'utf-8')).hexdigest()
        transaction15 = {**{"number": number15},**transaction15}
        
        self.txs_list.append(transaction15)         
        
        coin_input16 = []
        coin_input16.append({'number':transaction15['number'],'output':transaction15['output'][0]})
        coin_output16 = [{"value": 20, "pubkey": pk4.encode(encoder=HexEncoder).hex()},
                         {"value": 20, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 20, "pubkey": pk6.encode(encoder=HexEncoder).hex()},
                         {"value": 20, "pubkey": pk7.encode(encoder=HexEncoder).hex()},
                         {"value": 20, "pubkey": pk8.encode(encoder=HexEncoder).hex()}]
    
        transaction16 = {'input':coin_input16, 'output':coin_output16}
        signed16 = skcarol.sign(bytes(str(transaction16),'utf-8')).signature.hex()
        transaction16 = {**transaction16,**{"sig": signed16}}
        number16 = H(bytes(str(transaction16),'utf-8')).hexdigest()
        transaction16 = {**{"number": number16},**transaction16}
        
        self.txs_list.append(transaction16) 
        
        coin_input17 = []
        coin_input17.append({'number':transaction16['number'],'output':transaction16['output'][0]})
        coin_output17 = [{"value": 4, "pubkey": pk4.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk6.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk7.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk8.encode(encoder=HexEncoder).hex()}]
    
        transaction17 = {'input':coin_input17, 'output':coin_output17}
        signed17 = sk4.sign(bytes(str(transaction17),'utf-8')).signature.hex()
        transaction17 = {**transaction17,**{"sig": signed17}}
        number17 = H(bytes(str(transaction17),'utf-8')).hexdigest()
        transaction17 = {**{"number": number17},**transaction17}
        
        self.txs_list.append(transaction17) 
        
        #Miss field
        coin_input19 = []
        coin_input19.append({'number':transaction16['number'],'output':transaction16['output'][0]})
        coin_output19 = [{"value": 4, "pubkey": pk4.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk6.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk7.encode(encoder=HexEncoder).hex()},
                         {"value": 4, "pubkey": pk8.encode(encoder=HexEncoder).hex()}]
    
        transaction19 = {'output':coin_output19}
        signed19 = sk4.sign(bytes(str(transaction19),'utf-8')).signature.hex()
        transaction19 = {**transaction19,**{"sig": signed19}}
        number19 = H(bytes(str(transaction19),'utf-8')).hexdigest()
        transaction19 = {**{"number": number19},**transaction19}
        self.txs_list.append(transaction19) 
        
        #Input not equal to output
        coin_input20 = []
        coin_input20.append({'number':transaction16['number'],'output':transaction16['output'][1]})
        coin_input20.append({'number':transaction17['number'],'output':transaction17['output'][1]})
        coin_output20 = [{"value": 12, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 11, "pubkey": pk6.encode(encoder=HexEncoder).hex()}]
    
        transaction20 = {'input':coin_input20, 'output':coin_output20}
        signed20 = sk5.sign(bytes(str(transaction20),'utf-8')).signature.hex()
        transaction20 = {**transaction20,**{"sig": signed20}}
        number20 = H(bytes(str(transaction20),'utf-8')).hexdigest()
        transaction20 = {**{"number": number20},**transaction20}
        
        self.txs_list.append(transaction20)
        
        #Sinature is signed by different key
        coin_input21 = []
        coin_input21.append({'number':transaction16['number'],'output':transaction16['output'][1]})
        coin_input21.append({'number':transaction17['number'],'output':transaction17['output'][1]})
        coin_output21 = [{"value": 12, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 12, "pubkey": pk6.encode(encoder=HexEncoder).hex()}]
    
        transaction21 = {'input':coin_input21, 'output':coin_output21}
        signed21 = sk6.sign(bytes(str(transaction21),'utf-8')).signature.hex()
        transaction21 = {**transaction21,**{"sig": signed21}}
        number21 = H(bytes(str(transaction21),'utf-8')).hexdigest()
        transaction21 = {**{"number": number21},**transaction21}
        
        self.txs_list.append(transaction21)        
        
        #Hash is bad 
        coin_input22 = []
        coin_input22.append({'number':transaction16['number'],'output':transaction16['output'][1]})
        coin_input22.append({'number':transaction17['number'],'output':transaction17['output'][1]})
        coin_output22 = [{"value": 12, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 12, "pubkey": pk6.encode(encoder=HexEncoder).hex()}]
    
        transaction22 = {'input':coin_input22, 'output':coin_output22}
        signed22 = sk5.sign(bytes(str(transaction22),'utf-8')).signature.hex()
        transaction22 = {**transaction22,**{"sig": signed22}}
        number22 = H(b"Bad").hexdigest()
        transaction22 = {**{"number": number22},**transaction22}
        
        self.txs_list.append(transaction22)  
        
        
        
        
        coin_input18 = []
        coin_input18.append({'number':transaction16['number'],'output':transaction16['output'][1]})
        coin_input18.append({'number':transaction17['number'],'output':transaction17['output'][1]})
        coin_output18 = [{"value": 12, "pubkey": pk5.encode(encoder=HexEncoder).hex()},
                         {"value": 12, "pubkey": pk6.encode(encoder=HexEncoder).hex()}]
    
        transaction18 = {'input':coin_input18, 'output':coin_output18}
        signed18 = sk5.sign(bytes(str(transaction18),'utf-8')).signature.hex()
        transaction18 = {**transaction18,**{"sig": signed18}}
        number18 = H(bytes(str(transaction18),'utf-8')).hexdigest()
        transaction18 = {**{"number": number18},**transaction18}
        
        self.txs_list.append(transaction18)

        with open("transactions.json", "w") as outfile:
            json.dump(self.txs_list, outfile, indent=2)
            
            
            
    def main(self):
        #Read the transactions
        #self.crafting_transactions()
        
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
        # Start malicious node    
        Bad_Node(channels,self.pool,event,blockchains).run()    
        # Add to pool in 1s period  
        for i in range(len(transactions)-1):
            time.sleep(np.random.random(1)[0])
            self.pool.put(transactions[(i+1)])
         
        # Wait until all valid blocks are finished processing    
        flag = False
        counter = 0
        while flag == False:
            flag = True
            if counter > 180:
                print("Timeout in 1 minutes")
                break
            for i in blockchains:
                if len(i) != 16:
                    flag = False
            counter = counter+1
            time.sleep(1)
        
        
        print("Stopping!")
        #for thread_id, frame in sys._current_frames().items():
        #    print('Stack for thread {}'.format(thread_id))
        #    traceback.print_stack(frame)
        #    print('')
        event.set()
        #time.sleep(10)
        #print(self.pool.qsize())

        for i in range(nodes_num):  
            with open("block_chain_"+str(i)+".json", "w") as outfile:
                json.dump(blockchains[i], outfile, indent=2)   
        #while self.pool.qsize() > 0:
        #    print (self.pool.get()["number"]) 
    #def initialize_transaction(self,)            
            
        
if __name__ == "__main__":
	(Driver()).main()  