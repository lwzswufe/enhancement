# author='lwz'
# coding:utf-8
'''
多线程与线程间通讯
'''
import time
from threading import Thread, Event


MSG = []


def task_agent(thread_id=0):
    event_num = 0
    while True:
        event.wait()                # 阻塞 等待主线程唤醒
        event_num += 1
        if len(MSG) > 0:
            for msg in MSG:
                print("thread {} get {}".format(thread_id, msg))
                if msg == "stop":   # 退出循环 关闭子进程
                    print("thread {} end event_num: {}".format(thread_id, event_num))
                    return
        MSG.clear()
        event.clear()               # 重置event状态
        # time.sleep(0.01)          # 等待主线程关闭任务


def task_main():
    event_num = 0
    for i in range(100):
        MSG.append("str_{}".format(i))
        if i % 5 == 0:
            event.set()             # 开启event 唤醒子线程
            event_num += 1
            time.sleep(0.00001)     # 等待子线程执行

    MSG.append("stop")              # 关闭子线程
    event.set()                     # 唤醒子线程 让其自行关闭
    print("trread main event_num: {}".format(event_num))


if __name__ == "__main__":
    event = Event()
    th_0 = Thread(target=task_main, args=())
    th_list = [th_0]
    for i in range(1):
        th = Thread(target=task_agent, args=(i, ))
        th_list.append(th)
        th.start()
    st_time = time.time()
    th_0.start()
    for th in th_list:
        th.join()                   # 阻塞 等待子线程结束
    usetime = time.time() - st_time
    print("use {:.3f}s".format(usetime))
    


