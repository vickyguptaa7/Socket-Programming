import random
import socket
import threading
import json
import os
from xml.dom.expatbuilder import parseString
from xml.etree.ElementTree import tostring

os.system('cls||clear')

PORT = 4000
HEADER = 1024
FORMAT = "utf-8"
MAX_CLIENT = 2
DISCONNECT_MESSAGE = "!DISCONNECTED!"
FIRST_CONNECTION = "!FIRST_CONNECTION!"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
MAX_SIZE = 1000001

# creates a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

user_list = {}
isPrime = [True]*MAX_SIZE

# precomputation of all prime and comprime
def sieve_Of_Eratosthenes():
    global isPrime
    isPrime[0] = isPrime[1] = False
    for i in range(2, MAX_SIZE):
        j = i*i
        while (j < MAX_SIZE):
            isPrime[j] = False
            j += i


def sendMessage(msg, client_connection):
    client_connection.send(msg.encode(FORMAT))


def decodeMessage(str, client_connection, client_address):
    client_object = json.loads(str)
    if client_object['msg'] == FIRST_CONNECTION:
        # for first connection stores the name of the user corresponding to the client address
        global user_list, isPrime
        user_list[client_address] = {
            "name":  client_object['name'],
            "number": 2,
        }
        return f"joined the server."
    else:
        if (client_object['msg'] == 'start'):
            num = random.randrange(2, MAX_SIZE)
            user_list[client_address]['number'] = int(num)
            print(num)
            num = f"{num}"
            sendMessage(num, client_connection)
        else:
            num = user_list[client_address]['number']
            if (client_object['msg'] == 'p'):
                if (isPrime[num] == True):
                    sendMessage("Your answer is correct!", client_connection)
                else:
                    sendMessage("Your answer is incorrect!", client_connection)
            elif (client_object['msg'] == 'c'):
                if (isPrime[num] == False):
                    sendMessage("Your answer is correct!", client_connection)
                else:
                    sendMessage("Your answer is incorrect!", client_connection)
            else:
                sendMessage("Invalid Option!", client_connection)
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
    sieve_Of_Eratosthenes()
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
