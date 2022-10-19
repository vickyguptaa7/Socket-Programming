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

special_char = ["~", "`", "/", "\\", "?", ">", "<", ".",
                "!", ":", ";", "|", "=", "+", "-", "*", "@", "#", ]

# creates a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

user_list = {}


def sendMessage(msg, client_connection):
    client_connection.send(msg.encode(FORMAT))


def msgTypeDecide(msg):

    try:
        msg = int(msg)
        if msg < 0:
            return "-ve Integer"
        elif msg > 0:
            return "+ve Integer"
        else:
            return "Zero Integer"
    except:
        try:
            msg = float(msg)
            if msg > 0:
                return "+ve Float"
            elif msg < 0:
                return "-ve Float"
            else:
                return "Zero Float"
        except:
            if (msg.isalpha()):
                return "Alphabets"
            elif (msg.isalnum()):
                return "Alphanumeric"
            else:
                return "Special Characters"


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
        sendMessage(msgTypeDecide(client_object['msg']), client_connection)
        return client_object['msg']


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
