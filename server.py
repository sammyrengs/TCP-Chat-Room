import threading
import socket


#localhost
host = '127.0.0.1'
port = 37737


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clientlist = []
namelist = []

def broadcast(message):
    for client in clientlist:
            client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clientlist.index(client)
            clientlist.remove(client)
            client.close()
            name = namelist[index]
            broadcast(f'{name} left the chat!'.encode('ascii'))
            namelist.remove(name)
            break

def receive():
    while True:
        client,address = server.accept()
        print(f"Connected with {str(address)}")
        clientlist.append(client) 
        client.send('NAME:'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        namelist.append(name)
        print(f"Name of the client is {name}")
        broadcast(f'{name} joined the chat'.encode('ascii'))
        client.send(f'You have connected to the server'.encode('ascii'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print('Server is listening')
receive()