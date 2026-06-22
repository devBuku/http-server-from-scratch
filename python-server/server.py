import socket
from datetime import datetime, timezone

class TCPServer:
    response_headers ={ 
        'Server': 'HelloFriendServer',
        'Content-Type': 'text/html',
        }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        500: 'Internal Server Error'
    }
    
    def __init__(self, host = '127.0.0.1', port = 9999):
        self.host = host
        self.port = port
    
    def get_datetime(self):
        dt = datetime.now(timezone.utc)
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    def start_tcp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port)) 
        s.listen(10) 

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(1024)
            res_header = self.add_response_headers(200)
            res_body = self.add_response_body()
            blank_line = b"\r\n"
            res = b"".join([*res_header, blank_line, res_body])
            print(res)
            conn.sendall(data)
            conn.close()
            
    def add_response_headers(self, status_code = 500, extra_headers=None):
        line1 = f"HTTP/1.1 {status_code} {self.status_codes[status_code]}\r\n"
        new_header = self.response_headers.copy()
        if extra_headers:
            new_header.update(extra_headers)
        header = ""
        
        for h in new_header:
            header += f"{h}: {new_header[h]}\r\n"
            
        return [line1.encode(), self.get_datetime().encode(), header.encode()]
    
    def add_response_body(self):
        return  b"""<html><body><h1>Hello friend from HTML response</h1></body></html>"""
         
    def generate_response(self, data):
        return b"Hello friend!"  
   
if __name__ == "__main__":
    server = TCPServer()
    server.start_tcp()

