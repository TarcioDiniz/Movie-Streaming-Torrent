import random
import socket


def port_scanning():
    connect = 0
    while connect == 0:
        IP = socket.gethostbyname(socket.gethostname())
        PORT = random.randint(8000, 9000)

        createSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        createSocket.settimeout(0.6)
        connect = createSocket.connect_ex((IP, PORT))

        if connect != 0:
            return PORT


def accessTrue(ip, port):
    connect = 1
    while connect != 0:
        createSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        createSocket.settimeout(0.6)
        connect = createSocket.connect_ex((ip, port))
        if connect == 0:
            return False
        else:
            return True


def hostName():
    return socket.gethostbyname(socket.gethostname())
