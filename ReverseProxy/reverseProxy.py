import sys
import socket
import threading
import json

def readCurrentServer():
    currentServerFile = open("currentServer.txt", "r")
    current_server = int(currentServerFile.readline())
    currentServerFile.close()
    return current_server

def writeCurrentServer(current_server):
    currentServerFile = open("currentServer.txt", "w")
    currentServerFile.write(str(current_server))
    currentServerFile.close()

def delim():
    print("############################################")

class ReverseProxy:
    def __init__(self):
        with open('config.json') as config_file:
            self.config = json.load(config_file)
        self.backend_servers = []
        self.server_count = 0
        self.ipListFile = open(self.config['target_addr_file'], "r")
        for line in self.ipListFile.readlines():
            self.backend_servers.append(line[0:-1].split('://')[1])
            self.server_count += 1
        self.ipListFile.close()
        self.current_server = 0
        writeCurrentServer(self.current_server)

    def reverse_proxy(self, target, port, conn, data, addr):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target,port))
            s.send(data)
            while(1):
                reply = s.recv(self.config['buffer_size'])
                if(len(reply)>0):
                    conn.send(reply)
                    delim()
                    print("[*] Request done:")
                    print("\tAddress:", addr[0])
                    print("\tSize:", len(reply))
                    print(reply.decode('utf-8'))
                    delim()
                else:
                    break
        except socket.error as se:
            print("Encountered socket.error:", se)
        finally:
            s.close()
            conn.close()
            sys.exit(1)

    def forward_request(self, conn, data, addr):
        current_server = readCurrentServer()
        writeCurrentServer((current_server + 1)%self.server_count)
        target = self.backend_servers[current_server]
        target = target.split(':')
        server = target[0]
        port = int(target[1])

        self.reverse_proxy(server, port, conn, data, addr)

    def start(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.config['listen_addr'], self.config['listen_port']))
            s.listen(self.config['max_conn'])
            print("[*] Server started successfully at", (self.config['listen_addr'], self.config['listen_port']))
        except Exception as e:
            print("Encountered error", e)

        while 1:
            try:
                print("[*] Accepting connections")
                conn, addr = s.accept()
                print("[*] Accepted connection")
                data = conn.recv(self.config['buffer_size'])
                delim()
                print("[*] Recieved data => %s B <=" % str(len(data)))
                print(data.decode('utf-8'))
                delim()
                t = threading.Thread(target = self.forward_request, args = (conn, data, addr))
                t.start()
            except Exception as e:
                print("Encountered exception", e)
                print("[*] Proxy Shutdown...")
                s.close()
                sys.exit(2)

if __name__ == '__main__':
    reverseProxy = ReverseProxy()
    reverseProxy.start()
