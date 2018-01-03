# simple python chat server for multiple clients at once.

import socket
import threading

clients = []

client_name_lookup = {}

def send_all(name, message):
    global clients
    print(str(name+b': '+message,'UTF-8'))
    for client in clients:
        client.send(name)
        client.send(message)

def client_manager(client):
    global clients
    name = client_name_lookup[client]
    try:
        while True:
            send_all(name, client.recv(1024))
    except:
        clients.remove(client)
        client_name_lookup.pop(client, name)
        send_all(b"Server", name+b' Has Disconnected!')        

def on_connect(client):
    name = client.recv(32)
    client_name_lookup[client] = name
    send_all(b'Server', client_name_lookup[client] + b' Has Connected!')
    clients.append(client)

sock = socket.socket()
sock.bind((socket.gethostname(), 9339))
print("Connected as "+socket.gethostname()+", on port 9339.")
sock.listen(5)
while True:
    try:
        (client, address) = sock.accept()
        on_connect(client)
        threading.Thread(target=lambda: client_manager(client)).start()
    except:
        pass
