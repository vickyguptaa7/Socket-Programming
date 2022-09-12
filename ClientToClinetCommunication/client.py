from pickle import STOP
import socket
import json
import os
import sys
import threading
from time import sleep

os.system('cls||clear')


PORT = 4000
HEADER = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED!"
STOP_THREAD = False
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


def serverMessage():
    global STOP_THREAD
    while not STOP_THREAD:
        msg = client.recv(HEADER).decode(FORMAT)
        if len(msg) == 0:
            continue
        if msg == DISCONNECT_MESSAGE:
            break
        print(f"{msg}\n")


connected = True
while connected:
    thread = threading.Thread(target=serverMessage)
    thread.start()
    msg = input()
    print("")
    if msg == DISCONNECT_MESSAGE:
        # when program terminates the thread will also get terminates
        # To Close the working thread so that after program termination the thread is not active
        STOP_THREAD = True
        connected = False
        json_object = {'msg': msg}
        msg = json.dumps(json_object)
        sendMessage(msg)
        thread.join()
        
    json_object = {'msg': msg}
    msg = json.dumps(json_object)
    sendMessage(msg)


client.close()
print("[CLOSED]")
