import socket

client= socket.socket()
# IP = socket.gethostbyaddr("")
client.connect(("https://82ffbl9m-8080.inc1.devtunnels.ms",8080))

while True:
    print(client.recv(1024))
    client.send(input("Enter:-"))