import socket
import threading
import socketserver
import db
import time
import secrets

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

   
    def handle(self):
        #timeout control
        try:
            data = str(self.request.recv(1024), 'utf-8')
        except socket.timeout:
            print(self.client_address[0].strip()+"斷開連接")
            self.request.close()
            
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
                response = bytes("access fail","utf-8")
                self.request.sendall(response)
        elif(user[0]=="unlock"):
            if(dbc.user_search_token(user[1]!=None)):
                if(time.time()-dbc.user_search_time(user[1]) >= 120):
                    dbc.user_update_token("",0)
                    response = bytes("access timeout","utf-8")
                    self.request.sendall(response)
                #do unlock

        
            
    def finish(self):
            self.request.close()
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "10.200.23.135", 8080

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
    
    while(s!="off"):
        s = input("type off")
        if s == "off" :
            server.server_close()
            server.shutdown()
