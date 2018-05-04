import socket
import threading
import socketserver
import db
import time
import secrets

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        #timeout setting
        self.request.settimeout(120)
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, "Yes"), 'ascii')
        self.request.sendall(response)

    def handle(self):
        while(True):

            #timeout control
            try:
                data = str(self.request.recv(1024), 'ascii')
            except socket.timeout:
                print(self.client_address[0].strip()+"斷開連接")
                break
            
            user = data.split(" ")
            dbc = db.db_controler()

            #login fuction
            if(user[0]=="login"):
                if(dbc.user_search(user[1])!=None):
                    _token = secrets.token_hex(16)
                    _time = time.time()
                    dbc.user_update(_token,_time,user[1])
                    response = bytes(_token,"ascii")
                    self.request.sendall(response)
            #elif():control something
            #elif():control something

            
    def finish(self):
            print("{}: {}".format(cur_thread.name, "disconnect")
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 9999

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
