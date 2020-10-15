
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 9000))

# 开始监听
server.listen()

server.setblocking(False)


while True:
    # 在服务器端生成连接实例
    try:
        conn, addr = server.accept()
        while True:
            data = conn.recv(1024)
            print("receive data :", data)
            conn.send(data.upper())
            break
    except:
        print("No connection")


