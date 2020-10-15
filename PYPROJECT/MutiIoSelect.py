
# IO多路复用服务器端升级改造，读、写分离

import select
import socket
import queue


# 创建socket连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 4000))
server.listen(1000)


# 设置非阻塞模式
server.setblocking(False)


# key 为接受消息对象实例,key 为接受的数据
mes_dic = {}

# 需要检测的连接列表
# 自己也要监测,因为sk1本身也是个socket客户端
inputs = [server]

# 返回上一次的数据列表
outputs = []

while True:
    # 交给select去监控
    '''
    The return value is a tuple of three lists corresponding to the first three arguments; 
    each contains the subset of the corresponding file descriptors that are ready.
    '''
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)

    # 当rlist数组中的文件描述符发生可读时（可以调用accept或者read函数）
    for r in readable:
        # 当客户端第一次连接服务端时
        if r is server:
            conn, addr = server.accept()
            # 因为新建立的连接还没发数据过来,现在就接受的话程序就报错
            # 所以要想实现这个客户端发数据时server端能知道,就需要让select再监测
            inputs.append(conn)

            # 初始化一个队列,后面存要返回给这个客户端的数据
            mes_dic[conn] = queue.Queue()
        else:
           # 当客户端连接上服务端之后，再次发送数据时
           data = r.recv(1024)
           print("Receiving data", data)
           mes_dic[r].put(data)
           # 放入返回的连接队列里
           outputs.append(r)

    # 当wlist数组中的文件描述符发生可写时，则获取文件描述符添加到w数组中
    for w in writeable:
        data_to_client = mes_dic[w].get()
        # 读数据，处理数据,比如变成大写
        daata_to_client = data_to_client.upper()
        w.send(data_to_client)

        # 确保下次循环的时候writeable,不反回这个已经处理完的连接
        outputs.remove(w)

    # 异常
    for e in exceptional:
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)
        del mes_dic[e]
