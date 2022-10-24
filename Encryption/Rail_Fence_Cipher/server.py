import socket
import threading
import json
import os

os.system('cls||clear')

PORT = 4000
HEADER = 1024
FORMAT = "utf-8"
MAX_CLIENT = 2
DISCONNECT_MESSAGE = "!DISCONNECTED!"
FIRST_CONNECTION = "!FIRST_CONNECTION!"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

# creates a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

user_list = {}


def sendMessage(msg, client_connection):
    client_connection.send(msg.encode(FORMAT))


def decryptedMsg(msg, client_address):
    global user_list
    _key = int(user_list[client_address]['_key'])
    cols, rows = (len(msg), _key)
    mat = [[0 for i in range(cols)] for j in range(rows)]
    rowItr = 0
    isIncrement = True
    for i in range(cols):
        mat[rowItr][i] = '*'
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
    colItr = 0
    for r in range(rows):
        for c in range(cols):
            if (mat[r][c] == '*'):
                mat[r][c] = msg[colItr]
                colItr += 1
    decMsg = ""
    rowItr = 0
    isIncrement = True
    for i in range(cols):
        decMsg += mat[rowItr][i]
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
    return decMsg


def decodeMessage(str, client_connection, client_address):
    client_object = json.loads(str)
    if client_object['msg'] == FIRST_CONNECTION:
        # for first connection stores the name of the user corresponding to the client address
        global user_list
        user_list[client_address] = {
            "name":  client_object['name'],
            "connection": client_connection,
            "_key": client_object['_key']
        }
        return f"joined the server."
    else:
        msg = decryptedMsg(client_object['msg'], client_address)
        return msg


def handleClient(client_connection, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.\n")

    connected = True
    while connected:
        str = client_connection.recv(HEADER).decode(FORMAT)
        if len(str) == 0:
            continue

        msg = decodeMessage(str, client_connection, client_address)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            print(f"{user_list[client_address]['name']} is offline now.")
            continue
        print(f"{user_list[client_address]['name']} : {msg}")

    client_connection.close()


def start():
    server.listen(MAX_CLIENT)
    print(f"[LISTENING]  server is listening on {SERVER}\n")
    connected = True
    while connected:
        client_connection, client_address = server.accept()
        thread = threading.Thread(target=handleClient, args=(
            client_connection, client_address))
        thread.start()

        # -1 bcoz one thread is running the server
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}\n")


print("[STARTING] server is starting...\n")
start()
