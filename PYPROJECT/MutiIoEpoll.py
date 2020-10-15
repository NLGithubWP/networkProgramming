import socket
import select

# 创建套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 可重复绑定
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定本机地址端口
s.bind(("", 7788))

# 变为被动服务器
s.listen(1024)

# 创建一个epoll对象
epoll = select.epoll()

# 在epoll中注册s套接字(注意此处不是直接用是s, 而是使用s的fileno)
epoll.register(s.fileno(), select.EPOLLIN | select.EPOLLET)

# 创建两个字典, 来保存fileno和与其对应的套接字和地址
connections = {}
addresses = {}

# 开始等待客户端发送来的信息
while True:

    # 对epoll中的套接字进行扫描
    epollList = epoll.poll()

    # 对扫描到的事件进行判断
    for fd, events in epollList:

        # 如果判断是s套接字
        if fd == s.fileno():
            conn, addr = s.accept()

            print("有新的客户端到来...%s" % str(addr))
            connections[conn.fileno()] = conn
            addresses[conn.fileno()] = addr

            epoll.register(conn.fileno(), selecte.EPOLLIN | select.EPOLLET)

        # 如果是接收到了数据
        elif events == select.EPOLLIN:
            recvData = connections[fd].recv(1024)

            if len(recvData) > 0:
                print("recvData: %s" % recvData)

            else:
                epoll.unregister(fd)
                connections[fd].close()

                print("%s....offline....." % str(addresses[fd]))

