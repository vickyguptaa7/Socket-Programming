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


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def sendMessage(msg):
    client.send(msg.encode(FORMAT))


user_name = input("Enter your name : ")
_key = int(input("Enter the key : "))
json_object = {'name': user_name, 'msg': '!FIRST_CONNECTION!', "_key": _key}

msg = json.dumps(json_object)
sendMessage(msg)


def encryptMessage(msg):
    eText = ""
    global _key
    cols, rows = (len(msg), _key)
    mat = [[0 for i in range(cols)] for j in range(rows)]
    rowItr = 0
    isIncrement = True
    for i in range(cols):
        mat[rowItr][i] = msg[i]
        if isIncrement:
            if rowItr == rows-1:
                isIncrement = False
                rowItr -= 1
                continue
            rowItr += 1
        else:
            if rowItr == 0:
                isIncrement = True
                rowItr += 1
                continue
            rowItr -= 1
    # print(mat)
    for r in range(rows):
        for c in range(cols):
            if (mat[r][c] != 0):
                eText += mat[r][c]

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
    # server_msg = client.recv(HEADER).decode('utf8')
    # print(f"SERVER : {server_msg}")

client.close()
