import socket
import json
import os

os.system('cls||clear')


print("______________[CLIENT]_______________")
print("______Character And Word Count_______\n")

PORT = 4000
HEADER = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED!"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)


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


def sendMessage(msg):
    client.send(msg.encode(FORMAT))


user_name = input("Enter your name : ")
json_object = {'name': user_name, 'msg': '!FIRST_CONNECTION!'}

msg = json.dumps(json_object)
sendMessage(msg)


def countNumberAndCharacters(msg):
    integerCount = 0
    for i in range(len(msg)):
        if ord(msg[i]) >= 48 and ord(msg[i]) <= 57:
            integerCount += 1
    charCount = len(msg)-integerCount

    json_object = {
        'msg': f'Integer Count : {integerCount} \nCharacter Count : {charCount}'
    }
    return json_object


connected = True
while connected:
    server_msg = client.recv(HEADER).decode('utf8')
    print(f"SERVER : {server_msg}")

    client_msg = countNumberAndCharacters(server_msg)
    msg = json.dumps(client_msg)
    sendMessage(msg)
    print(f"You :\n {client_msg['msg']}")

client.close()
