#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 13:30:14 2022

@author: mat
"""
from multiprocessing.connection import Listener
from multiprocessing import Process, Manager
from multiprocessing.connection import Client
import sys
from time import time
import traceback


# client_info = {'msg','name','address','authkey'm'port'}

def send_msg(conn,msg,info):
    
    with Client(address=(info['address'],info['port']),authkey=info['authkey']) as conn:
        conn.send(msg)


def manage(conn,lock,database):
    
    while True:
        try:
            temp= conn.recv()
            order,client_info = temp['order'], temp['info']
            info_to_add = {'nickname':client_info['name'], 'address':client_info['address']}

            if order == '__join__':
                database.append(info_to_add)
                print(f'client {client_info["name"]} is now online')               
            elif order == '__quit__':
                print(f'client {client_info["name"]} is offline')
                break  
            else:
                print(order)                      
        except:
            print(f'client {client_info["name"]} apparently crashed')
            traceback.print_exc()
            break
        
    database.remove(info_to_add)
    conn.close()
    print(f'client {client_info["name"]} removed from database')
    


if __name__ == '__main__':
    
    ip_address ='127.0.0.1'
    server_port = 6000
    if len(sys .argv)>1:
        ip_address = sys.argv[1]
        
    with Listener(address=(ip_address, server_port),authkey=b'secret password server') as listener:
        print('listener starting')  
        m = Manager()
        database = m.list()
        lock = m.Lock()
        
        while True:
            try:
                conn = listener.accept()
                print ('connection accepted from', listener.last_accepted)
                p = Process(target=manage, args=(conn,lock,database))
                p.start()
            except:
                traceback.print_exc()
            
            