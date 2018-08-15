# author='lwz'
# coding:utf-8
'''
多线程与线程间通讯
'''
import time
from threading import Thread
import socket
import random
import sys


def get_timestr():
    now = time.time()
    str_1 = time.strftime("%H:%M:%S", time.localtime(now))
    str_2 = "{:.3f}".format(now % 1)
    return str_1 + str_2


def connect(address, source_address, timeout):
    try:
        client = socket.create_connection(address=address, source_address=source_address, timeout=timeout)
    except OSError as err:
        print(err)
        raise OSError
    except Exception as err:
        print(err)
        raise OSError
    print("client: {}".format(client.getsockname()))
    return client


def task_agent(thread_id, host, port):
    flag_0 = 0
    client = connect((host, port), (host, port - 1), 1)
    while True:
        try:
            data = client.recv(1024)    # 阻塞 等待主线程唤醒
        except socket.timeout:
            continue
        except Exception as err:
            print(err)
            client.close()
            del client
            client = connect((host, port), (host, port - 1), 1)
        if len(data) > 0:
            timestr = get_timestr()
            print("{} thread {} get {}".format(timestr, thread_id, data.decode()))
        else:
            flag_0 += 1
            if flag_0 > 10:
                client.close()
                del client
                return
        if data == b"stop":
            print("thread {} end".format(thread_id))
            client.close()
            del client
            return


def task_main(host, port):
    client = connect((host, port), (host, port + 1), 1)
    for i in range(10):
        timestr = get_timestr()
        send_str = "str_{}".format(i)
        try:
            client.send(send_str.encode())
        except Exception as err:
            print(send_str)
            print(err)
            client.close()
            del client
            client = connect((host, port), (host, port - 1), 1)
        print("{} send {}".format(timestr, send_str))
        time.sleep(random.random() * 5)

    timestr = get_timestr()
    send_str = "stop"
    client.send(send_str.encode())
    print("{} send {}".format(timestr, send_str))
    client.close()
    del client


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 7005
    th_0 = Thread(target=task_main, args=(host, port))
    for i in range(1):
        th = Thread(target=task_agent, args=(i, host, port + i + 1))
        th.start()
    th_0.start()