# author='lwz'
# coding:utf-8
'''
多线程与线程间通讯
'''
import time
from threading import Thread, Event


MSG = []


def task_agent(thread_id=0):
    while True:
        event.wait()                # 阻塞 等待主线程唤醒
        if len(MSG) > 0:
            for msg in MSG:
                print("thread {} get {}".format(thread_id, msg))
                if msg == "stop":   # 退出循环 关闭子进程
                    print("thread {} end".format(thread_id))
                    return
        time.sleep(0.2)             # 等待主线程关闭任务


def task_main():
    for i in range(10):
        MSG.append("str_{}".format(i))
        if i in [2, 3, 5, 7, 9]:
            event.set()             # 开启event 唤醒子线程
            time.sleep(0.18)        # 等待子线程执行
            MSG.clear()             # 清空缓存数据
            event.clear()           # 重置event状态
            print(MSG)
    MSG.append("stop")              # 关闭子线程
    event.set()                     # 唤醒子线程 让其自行关闭


if __name__ == "__main__":
    event = Event()
    th_0 = Thread(target=task_main, args=())
    th_list = [th_0]
    for i in range(3):
        th = Thread(target=task_agent, args=(i, ))
        th_list.append(th)
        th.start()
    th_0.start()
    for th in th_list:
        th.join()                   # 阻塞 等待子线程结束
    


