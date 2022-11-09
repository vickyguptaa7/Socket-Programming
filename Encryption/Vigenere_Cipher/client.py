from ast import Global
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

vigMatrix = [[0 for i in range(26)] for j in range(26)]


def intializeVigMatrix():
    global vigMatrix
    for r in range(26):
        for c in range(26):
            vigMatrix[r][c] = chr((r+c) % 26+65)


intializeVigMatrix()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def sendMessage(msg):
    client.send(msg.encode(FORMAT))


user_name = input("Enter your name : ")
_key = input("Enter the key : ").upper()
json_object = {'name': user_name, 'msg': '!FIRST_CONNECTION!', "_key": _key}

msg = json.dumps(json_object)
sendMessage(msg)


def encryptMessage(msg):
    global _key, vigMatrix
    keyConcat = ""
    times = int(len(msg)/len(_key))
    for i in range(times):
        keyConcat += _key
    keyConcat += _key[0:len(msg)-len(_key)*times]

    print(keyConcat)

    encMessage = ""
    for i in range(len(msg)):
        r = ord(keyConcat[i])-65
        c = ord(msg[i])-65
        encMessage += vigMatrix[r][c]
    return encMessage


connected = True
while connected:
    msg = input("Enter a message : ").upper()
    if msg == DISCONNECT_MESSAGE:
        connected = False
        continue
    msg = encryptMessage(msg)
    json_object = {'msg': msg}
    msg = json.dumps(json_object)

    print(f"[MESSAGE SENT TO SERVER] : {msg}")
    sendMessage(msg)
    server_msg = client.recv(HEADER).decode('utf8')
    print(f"SERVER : {server_msg}")

client.close()
