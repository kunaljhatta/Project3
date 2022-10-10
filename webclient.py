import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])
s = socket.socket()
s.connect((host,port))

request = "GET / HTTP/1.1\r\nHost:{}\r\nConnection: close\r\n\r\n".format(host)
s.sendall(request.encode("ISO-8859-1"))

data = []
while True:
    responses = s.recv(4096)
    if not responses:
        break
    print(responses.decode("ISO-8859-1"))
    data.append(responses)

print("Connection successfully ended!")
s.close()