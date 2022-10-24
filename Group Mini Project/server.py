import random
import socket
import threading
import json

print("\033c")

PORT = 4000
# size of data in bytes that can go in one packets
HEADER = 1024
FORMAT = "utf-8"
MAX_CLIENT = 2
DISCONNECT_MESSAGE = "!DISCONNECTED!"
FIRST_CONNECTION = "!FIRST_CONNECTION!"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
MAX_SIZE = 1000001

# stores the client information like username
user_list = {}

# store the information that number is prime or composite
# True means prime and False means composite
isPrime = [True]*MAX_SIZE

"""
Here we made a socket instance and passed it two parameters. The first parameter is AF_INET and the second one is SOCK_STREAM. AF_INET refers to the address-family ipv4. The SOCK_STREAM means connection-oriented TCP protocol.  
"""
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print(f"[UNABLE TO CREATE SOCKET] : {err}...\n")
    exit(0)

"""
A server has a bind() method which binds it to a specific IP and port so that it can listen to incoming requests on that IP and port.  
"""
try:
    server.bind(ADDRESS)
except socket.error as err:
    print(f"[UNABLE TO BIND TO THE SPECIFIC IP AND PORT] : {err}...\n")
    exit(0)


# precomputes all prime and composite in the range of 2, MAX_SIZE
def sieve_Of_Eratosthenes():
    global isPrime
    isPrime[0] = isPrime[1] = False
    for i in range(2, MAX_SIZE):
        j = i*i
        while (j < MAX_SIZE):
            isPrime[j] = False
            j += i

# send message to the client


def sendMessage(msg, client_connection, client_address):
    try:
        client_connection.send(msg.encode(FORMAT))
    except socket.error as err:
        global user_list
        print(
            f"[UNABLE TO SEND MESSAGE TO THE {user_list[client_address]['name']}] : {err}...\n")
        del user_list[client_address]
        # exit the helper thread created not the main thread
        exit(0)

# decode the message if it was the first message or the other message and respond accordingly


def decodeMessage(str, client_connection, client_address):
    client_object = json.loads(str)
    if client_object['msg'] == FIRST_CONNECTION:
        # for first connection stores the name of the user corresponding to the client address and the number which
        # is to be send
        global user_list, isPrime
        user_list[client_address] = {
            "name":  client_object['name'],
            "number": 2,
        }
        return f"joined the server."
    else:
        if (client_object['msg'] == 'start'):
            # start the game message so we have to send a random number to the client
            num = random.randrange(2, MAX_SIZE)
            user_list[client_address]['number'] = int(num)
            print(num)
            num = f"{num}"
            sendMessage(num, client_connection, client_address)
        else:
            # its the respose from the client of the game so we have to check whether its correct or not
            num = user_list[client_address]['number']
            if (client_object['msg'] == 'p'):
                if (isPrime[num] == True):
                    sendMessage("Your answer is correct!",
                                client_connection, client_address)
                else:
                    sendMessage("Your answer is incorrect!",
                                client_connection, client_address)
            elif (client_object['msg'] == 'c'):
                if (isPrime[num] == False):
                    sendMessage("Your answer is correct!",
                                client_connection, client_address)
                else:
                    sendMessage("Your answer is incorrect!",
                                client_connection, client_address)
            else:
                sendMessage("Invalid Option!",
                            client_connection, client_address)

        return client_object['msg']

# handle's client queries


def handleClient(client_connection, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.\n")
    global user_list
    connected = True
    while connected:
        # reciveing response from client
        try:
            str = client_connection.recv(HEADER).decode(FORMAT)
        except socket.error as err:
            print(
                f"[UNABLE TO RECIVE MESSAGE FROM THE {user_list[client_address]['name']}] : {err}...\n")
            del user_list[client_address]
            # exit the helper thread created not the main thread
            exit(0)

        if len(str) == 0:
            continue

        msg = decodeMessage(str, client_connection, client_address)
        if msg == DISCONNECT_MESSAGE:
            # disconnect the client from the server if message is !DISCONNECTED!
            connected = False
            print(f"{user_list[client_address]['name']} is offline now.")
            continue

        print(f"{user_list[client_address]['name']} : {msg}")

    # removing the client from the list after he/she get disconnected
    del user_list[client_address]
    client_connection.close()


def start():
    """
    A server has a listen() method which puts the server into listening mode. This allows the server to listen to incoming connections.
    """
    server.listen(MAX_CLIENT)
    sieve_Of_Eratosthenes()
    print(f"[LISTENING]  server is listening on {SERVER}\n")
    connected = True
    while connected:
        """
        And last a server has an accept() and close() method. The accept method initiates a connection with the client and the close method closes the connection with the client. 
        """
        try:
            client_connection, client_address = server.accept()
        except socket.error as err:
            print(f"[UNABLE TO CONNECT TO THE CLIENTS] : {err}...\n")
            exit(0)

        try:
            thread = threading.Thread(target=handleClient, args=(
                client_connection, client_address))
            thread.start()
        except socket.error as err:
            print(f"[UNABLE TO CREATE THREAD] : {err}...\n")
            exit(0)

        # -1 bcoz one thread is running the server
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}\n")


print("[STARTING] server is starting...\n")
start()
