
import socket


if "__main__" == __name__:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 4000))
    sock.send(b'cc1')

    data = sock.recv(1024)
    print(data)
    sock.close()
