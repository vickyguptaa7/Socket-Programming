import socket
import json
import os

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
json_object = {'name': user_name, 'msg': '!FIRST_CONNECTION!'}

msg = json.dumps(json_object)
sendMessage(msg)

connected = True
while connected:
    msg = input("Play a game [y/n]: ")

    if (msg != 'y'):
        if msg != 'n':
            print("Invalid Option!")
        msg = DISCONNECT_MESSAGE
        connected = False
        json_object = {'msg': msg}
        msg = json.dumps(json_object)
        sendMessage(msg)
        continue

    json_object = {'msg': 'start'}
    msg = json.dumps(json_object)
    sendMessage(msg)

    server_msg = client.recv(HEADER).decode('utf8')
    print(f"Server : {server_msg}")

    msg = input("Prime or Composite [p/c] : ")

    json_object = {'msg': msg}
    msg = json.dumps(json_object)
    sendMessage(msg)

    server_msg = client.recv(HEADER).decode('utf8')
    print(f"Server : {server_msg}")

print("Connection Closed!")
client.close()
