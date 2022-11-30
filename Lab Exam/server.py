from curses.ascii import isalnum
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


def decodeMessage(str, client_connection, client_address):
    client_object = json.loads(str)
    if client_object['msg'] == FIRST_CONNECTION:
        # for first connection stores the name of the user corresponding to the client address
        global user_list
        user_list[client_address] = {
            "name":  client_object['name'],
            "connection": client_connection,
        }
        return f"joined the server."
    else:
        return client_object['msg']


def handleClient(client_connection, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.\n")

    connected = True
    while connected:
        str = client_connection.recv(HEADER).decode(FORMAT)
        if len(str) == 0:
            continue

        msg = decodeMessage(str, client_connection, client_address)
        print(f"{user_list[client_address]['name']} : \n{msg}")
        msg = input("Enter The String : ")
        sendMessage(msg, client_connection)

    client_connection.close()


def start():
    server.listen(MAX_CLIENT)
    print(f"[LISTENING]  server is listening on {SERVER}\n")
    connected = True
    while connected:
        client_connection, client_address = server.accept()
        handleClient(client_connection, client_address)


print("[STARTING] server is starting...\n")
start()
