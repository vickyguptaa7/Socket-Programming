import socket
import json

print("\033c")

PORT = 4000
# size of data in bytes that can go in one packets
HEADER = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED!"

# get the server ip address

SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)


"""
Here we made a socket instance and passed it two parameters. The first parameter is AF_INET and the second one is SOCK_STREAM. AF_INET refers to the address-family ipv4. The SOCK_STREAM means connection-oriented TCP protocol.
"""

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print(f"[UNABLE TO CREATE SOCKET] : {err}...\n")
    exit(0)
try:
    # coneecting the client to the server
    client.connect(ADDRESS)
except socket.error as err:
    print(f"[UNABLE TO CONNECT TO THE SERVER] : {err}...\n")
    exit(0)


# function to send message to the server
def sendMessage(msg):
    json_object = {'msg': msg}
    msg = json.dumps(json_object)
    try:
        client.send(msg.encode(FORMAT))
    except socket.error as err:
        print(f"[UNABLE TO SEND MESSAGE TO THE SERVER] : {err}...\n")
        exit(0)


def reciveMessage():
    try:
        server_msg = client.recv(HEADER).decode('utf8')
    except socket.error as err:
        print(f"[UNABLE TO RECIEVE MESSAGE FROM THE SERVER] : {err}...\n")
        exit(0)
    print(f"Server : {server_msg}")
    return server_msg


"""
This is the first message sent to the server from the client side to know that another client is connected 
so we have to store the client information and don't ask the info again and again from the client side
"""

user_name = input("Enter your name : ")
json_object = {'name': user_name, 'msg': '!FIRST_CONNECTION!'}
msg = json.dumps(json_object)
client.send(msg.encode(FORMAT))

connected = True
while connected:
    print("\033c")
    print("_______[GAME_SERVER]________\n")
    msg = input("Play a game [y/n]: ")

    if (msg != 'y'):
        if msg != 'n':
            print("Invalid Option!")

        # user don't want to play the game
        msg = DISCONNECT_MESSAGE
        connected = False
        sendMessage(msg)
        continue

    # client response to the server that user wants to play the game
    sendMessage('start')

    # server response to the client with a question
    server_msg = reciveMessage()

    # client response to the server to answer the question
    msg = input("Prime or Composite [p/c] : ")
    sendMessage(msg)

    # server response to the client wheter the answer is correct or not
    server_msg = reciveMessage()

    input("Press Enter to continue...")

# closing the connection fromt the server
print("Connection Closed!")
client.close()
