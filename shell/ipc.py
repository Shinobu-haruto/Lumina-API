
import socket
import json

HOST = "127.0.0.1"
PORT = 45820


class IPCServer:

    def __init__(self, handler):
        self.handler = handler

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()

        print("Lumina ShellHost IPC iniciado")

        while True:
            conn, _ = server.accept()

            data = conn.recv(4096).decode()
            message = json.loads(data)

            self.handler(message)

            conn.close()


def send(message):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.send(json.dumps(message).encode())
    client.close()
