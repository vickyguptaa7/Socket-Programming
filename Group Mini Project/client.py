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
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# coneecting the client to the server
client.connect(ADDRESS)


# function to send message to the server
def sendMessage(msg):
    client.send(msg.encode(FORMAT))


"""
This is the first message sent to the server from the client side to know that another client is connected 
so we have to store the client information and don't ask the info again and again from the client side
"""
user_name = input("Enter your name : ")
json_object = {'name': user_name, 'msg': '!FIRST_CONNECTION!'}
msg = json.dumps(json_object)
sendMessage(msg)

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
        json_object = {'msg': msg}
        msg = json.dumps(json_object)
        sendMessage(msg)
        continue

    # client response to the server that user wants to play the game
    json_object = {'msg': 'start'}
    msg = json.dumps(json_object)
    sendMessage(msg)

    # server response to the client with a question
    server_msg = client.recv(HEADER).decode('utf8')
    print(f"Server : {server_msg}")

    # client response to the server to answer the question
    msg = input("Prime or Composite [p/c] : ")
    json_object = {'msg': msg}
    msg = json.dumps(json_object)
    sendMessage(msg)

    # server response to the client wheter the answer is correct or not
    server_msg = client.recv(HEADER).decode('utf8')
    print(f"Server : {server_msg}")
    input("Press Enter to continue...")

# closing the connection fromt the server
print("Connection Closed!")
client.close()
