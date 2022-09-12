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

USERS_NAME_LIST = {}
USER_CONNECTION_LIST = {}
ALL_MESSAGES = ""


def sendMessage(msg, client_connection):
    client_connection.send(msg.encode(FORMAT))


def broadcastMessage(msg, client_address):
    for c_address in USER_CONNECTION_LIST:
        if c_address == client_address:
            continue
        sendMessage(msg, USER_CONNECTION_LIST[c_address])


def decodeMessage(str, client_address, client_connection):
    client_object = json.loads(str)
    if client_object['msg'] == FIRST_CONNECTION:
        # for first connection stores the name of the user corresponding to the client address
        USERS_NAME_LIST[client_address] = client_object['name']
        USER_CONNECTION_LIST[client_address] = client_connection
        sendMessage(ALL_MESSAGES, client_connection)
        return f"[JOINED THE SERVER]"
    else:
        return client_object['msg']


def handleClient(client_connection, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.\n")

    connected = True
    while connected:
        str = client_connection.recv(HEADER).decode(FORMAT)
        if len(str) == 0:
            continue
        global ALL_MESSAGES
        msg = decodeMessage(str, client_address, client_connection)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            msg = f"{USERS_NAME_LIST[client_address]} is offline now."
            ALL_MESSAGES += "\n"+msg
            broadcastMessage(msg, client_address)
            # to take down the user thread
            sendMessage(DISCONNECT_MESSAGE, client_connection)
            continue

        msg = f"{USERS_NAME_LIST[client_address]} : {msg}"
        ALL_MESSAGES += "\n"+msg
        broadcastMessage(msg, client_address)

    # Removing the user who got disconnected
    del USERS_NAME_LIST[client_address]
    del USER_CONNECTION_LIST[client_address]
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
