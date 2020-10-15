
import socket
import time

if "__main__" == __name__:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 4000))
    while 1:
        sock.send(b'cc4')

        data = sock.recv(1024)
        print(data)
        time.sleep(5)
    sock.close()
