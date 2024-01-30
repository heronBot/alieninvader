import socket

server = socket.socket()
server.bind(("",8080))
server.listen()
c,a = server.accept()

while True:
    c.send(input("Enter:-"))
    print(c.recv(1024))