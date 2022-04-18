#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 14:01:43 2022

@author: mat
"""
from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Lock
from multiprocessing.connection import Client
import sys
from time import time

# client_info = {'msg','name','address','authkey'm'port'}
        

if __name__ == '__main__':
    
    server_address = '127.0.0.1'
    server_port = 6000
    port = 6001
    authkey=b'secret client server'
    if len(sys .argv)>1:
        server_address = sys.argv[1]
    if len(sys .argv)>2:
        port = int(sys.argv[2])
    
    name = input('Your name to use: ')
    address = input('Your ip_address: ')
    
    client_info = {'name':name,'address':address,'authkey':authkey,'port':port}  
    
    with Client(address=(server_address, server_port),authkey=b'secret password server') as conn:
        
        to_server = {'order':'__join__','info':client_info}   
        conn.send(to_server)

        while True:
            msg = input('enter message ("__quit__" will exit): ')
            if msg == "__quit__":
                to_server['order'] = msg
                conn.send(to_server)
                break
            else:
                to_server['order'] = msg
                conn.send(to_server)
               
        print('client exited')
