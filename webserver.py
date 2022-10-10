import socket
import sys
import os

port = int(sys.argv[1])
s = socket.socket()
s.bind(('', port))
s.listen()

ext_mapping = {'.txt':'text/plain', '.html':'text/html'}

def recieve_data(data):
    encoded_req = data.recv(4096)
    request = ""
    while True:
        decoded_req = encoded_req.decode("ISO-8859-1")
        request = request + decoded_req
        if decoded_req.find('\r\n\r\n'):
            return request

while True:
    new_conn = s.accept()
    new_socket = new_conn[0]  
    header_data = recieve_data(new_socket) 
    get = header_data.split("\r\n")
    method = get[0].split()[0]
    path = get[0].split()[1]
    protocol = get[0].split()[2]
    file_path = os.path.split(path)[1]
    file_extension = os.path.splitext(file_path)[1]
        
    try:
        with open(file_path) as fp:
            data = fp.read()   
            data_length = data.encode("ISO-8859-1")
            length = len(data_length)
            response = ("HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}").format(ext_mapping[file_extension], length, data)
            new_socket.sendall(response.encode("ISO-8859-1"))
    except:
           response = ("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found")
           new_socket.sendall(response.encode("ISO-8859-1"))

    new_socket.close()