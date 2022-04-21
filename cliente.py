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
import traceback

# client_info = {'name','address','authkey','port'}
        

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
        
        to_server = {'request':'__join__','info':client_info}   
        conn.send(to_server)
        print(conn.recv())

        while True:
            msg = input('enter (__help__ for command menu): ')
            if msg == '__help__':
                print('Commands for server interaction: __help__, __refresh__, __quit__')
            elif msg == "__quit__":
                to_server['request'] = msg
                conn.send(to_server)
                break
            elif msg == '__refresh__':
                to_server['request'] = msg
                conn.send(to_server)
                print(conn.recv())
            elif msg == '__talk__':
                name = input('Enter user nickname: ')
                to_server['request'] = msg
                to_server['user'] = name
                conn.send(to_server)
                print(conn.recv())
               
    print('client exited')
