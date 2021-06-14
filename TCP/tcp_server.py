import socket


class TCPServer(object):
    def __init__(self):
        # 创建socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口复用
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket = None

    def listen(self, ip, port):
        # 获取地址
        server_addr = (ip, port)
        # 绑定socket
        self.socket.bind(server_addr)
        # 等待连接
        self.socket.listen(128)
        self.client_socket, client_addr = self.socket.accept()
        # 发送数据
        hello = "Hello I'm Server"
        self.client_socket.send(hello.encode("utf-8"))
        # 接受数据
        recv_byte = self.client_socket.recv(1024)
        recv_str = recv_byte.decode('utf-8')
        print("get:{} from:{}".format(recv_str, client_addr))

    def send(self, string):
        self.client_socket.send(string.encode("utf-8"))

    def unconnect(self):
        # 关闭套接字
        self.send("unconnect")
        self.client_socket.close()



def main():
    import time
    server = TCPServer()
    server.listen("127.0.0.1", 8888)
    for i in range(20):
        msg = "message{:03d}".format(i);
        server.send(msg)
        time.sleep(0.2)
    server.unconnect()


if __name__ == "__main__":
    main()