import socket


class TCPClient(object):
    def __init__(self):
        # 创建socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        # 连接服务器
        server_addr = (ip, port)
        self.socket.connect(server_addr)
        # 接收数据
        recv_str = self.recv()
        print("Client get:{}".format(recv_str))
        # 发送数据
        hello = "Hello I'm Client"
        self.socket.send(hello.encode("utf-8"))

    def recv(self):
        # 接收数据
        recv_byte = self.socket.recv(1024)
        recv_str = recv_byte.decode("utf-8")
        return recv_str

    def unconnect(self):
        # 4. 关闭套接字
        self.socket.close()



def main():
    import time
    client = TCPClient()
    client.connect("127.0.0.1", 8888)
    while(True):
        msg = client.recv()
        if len(msg) > 0:
            print("get:{}".format(msg))
        if msg == "unconnect":
            print("client exit")
            break
        time.sleep(0.1)
    client.unconnect()


if __name__ == "__main__":
    main()