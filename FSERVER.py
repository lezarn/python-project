#!/usr/bin/env python3.6
import socket
import threading
import socketserver
import db
import time
import secrets
#import RPi.GPIO as GPIO
from time import sleep
from queue import Queue

"""
GPIO.setmode(GPIO.BCM)
lock = 18

GPIO.setwarnings(False)
GPIO.setup(lock,GPIO.OUT)

"""
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    """def setup(self):
        try:
            pubkey=load_pkcs1('publickey.pem')
            prikey=load_pkcs1('privatekey.pem')

        except Exception :
            self.request.close()

        else:
            pass"""
            
   
    def handle(self):
        
        #timeout control
        try:
            data = str(self.request.recv(1024), 'utf-8')
            self.subthreadjob(data)
            
        except socket.timeout:
            print(self.client_address[0].strip()+"斷開連接")
            self.request.close()
            
                    
            
    def finish(self):
        self.request.close()




    def subthreadjob(self, data):
        user = data.split(" ")
        dbc = db.db_controler()
        #login fuction
        if(user[0]=="login"):
            if(dbc.user_login(user[1],user[2])!=None):
                _token = secrets.token_hex(16)
                _time = time.time()
                dbc.user_update(_token,_time,user[1])
                response = bytes("success "+_token,"utf-8")
                self.request.sendall(response)
            else:
                response = bytes("帳號或密碼錯誤!!","utf-8")
                self.request.sendall(response)
        elif(user[0]=="unlock"):
            q.put("token error")
            if(dbc.user_search_token(user[1])!=None):
                q.put("time error")
                if(time.time()-dbc.user_search_time(user[1])[0] >= 120):
                    dbc.user_update_bytoken("",0)
                    q.put("fail")
                    
                """else:
                    user_update_bytoken(user[1], time.time())
                    GPIO.output(lock, 1)
                    sleep(1)
                    GPIO.output(lock, 0)
                    #do unlock"""
                

        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass




if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "192.168.0.13", 8080

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    s = ""

    q=Queue()
    
    while(s!="off"):
        s = input("type off")
        if s == "off" :
            while not q.empty():
                print(q.get())
            server.server_close()
            server.shutdown()
