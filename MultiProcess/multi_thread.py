# author='lwz'
# coding:utf-8
'''
多线程与线程间通讯
'''
import time
from threading import Thread, Event
from collections import deque

MSG = deque()


def task_agent(thread_id=0):
    event_num = 0
    while True:
        event.wait()                # 阻塞 等待主线程唤醒
        event.clear()
        event_num += 1
        while len(MSG) > 0:
            msg = MSG.popleft()
            print("thread {} get {}".format(thread_id, msg))
            if msg == "stop":   # 退出循环 关闭子进程
                print("thread {} end event_num: {}".format(thread_id, event_num))
                return
        # time.sleep(0.01)          # 等待主线程关闭任务


def task_main(thread_num):
    event_num = 0
    for i in range(20):
        MSG.append("str_{}".format(i))
        if i % 5 == 0:
            event.set()            # 开启event 唤醒子线程
            event_num += 1
            time.sleep(0.001)      # 等待子线程执行

    for i in range(thread_num):
        MSG.append("stop")         # 关闭子线程
        event.set()                # 唤醒子线程 让其自行关闭
    print("trread main event_num: {}".format(event_num))


if __name__ == "__main__":
    event = Event()
    thread_num = 5                 # 子线程数量
    th_0 = Thread(target=task_main, args=(thread_num, ))
    th_list = [th_0]
    for i in range(thread_num):
        th = Thread(target=task_agent, args=(i, ))
        th_list.append(th)
        th.start()
    st_time = time.time()
    th_0.start()
    for th in th_list:
        th.join()                   # 阻塞 等待子线程结束
    usetime = time.time() - st_time
    print("use {:.3f}s".format(usetime))
    


