import socket
import json
import os
from array import *
os.system('cls||clear')


PORT = 4000
HEADER = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED!"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def sendMessage(msg):
    client.send(msg.encode(FORMAT))


user_name = input("Enter your name : ")
_key = 3
json_object = {'name': user_name, 'msg': '!FIRST_CONNECTION!', "_key": _key}

msg = json.dumps(json_object)
sendMessage(msg)


def encryptMessage(msg):
    eText = ""
    global _key

    for i in range(len(msg)):
        eText += chr((ord(msg[i])-97+_key) % 26+97)

    return eText


connected = True
while connected:
    msg = input("Enter a message : ")
    if msg == DISCONNECT_MESSAGE:
        connected = False
    msg = encryptMessage(msg)
    json_object = {'msg': msg}
    msg = json.dumps(json_object)

    print(msg)
    sendMessage(msg)

client.close()
