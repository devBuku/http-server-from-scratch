import socket


class TCPServer:
    def __init__(self, host = '127.0.0.1', port = 9999):
        self.host = host
        self.port = port
    
    
    def start_tcp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port)) 
        s.listen(10) 

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(1024)
            res = self.generate_response(data)
            print(res)
            conn.sendall(data)
            conn.close()
        
    def generate_response(self, data):
        return b"Hello friend!"  

if __name__ == "__main__":
    server = TCPServer()
    server.start_tcp()

