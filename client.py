import threading
import socket
import re
import colorama
from colorama import init, Fore

init(autoreset=True)

name = input('Enter your name: ')


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',37737))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NAME:':
                client.send(name.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occurred')
            client.close()
            break

def write():
    while True:
        message = f'{name}: {input("")}'
        if message == "/leave":
            client.close()
        if re.search("/color",str(message)):
            res = re.split(r"<|>",str(message))
            color = res[1].upper()
            if(color == 'RED'):
                color = Fore.RED
            elif(color == 'BLUE'):
                color = Fore.BLUE
            elif(color == 'YELLOW'):
                color = Fore.YELLOW
            elif(color == 'GREEN'):
                color = Fore.GREEN
            else:
                color = Fore.WHITE
            message1 = res[2]
            message1 = f"{color} {message1}{Fore.RESET}"
            client.send(message1.encode('ascii'))
        else:
            client.send(message.encode('ascii'))
        
receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()