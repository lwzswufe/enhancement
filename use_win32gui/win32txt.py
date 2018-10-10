# author='lwz'
# coding:utf-8
import win32gui, win32con
win = win32gui.FindWindow(None, u'无标题.txt - 记事本')
tid = win32gui.FindWindowEx(win, None, 'Edit', None)
win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, 'hello')
win32gui.PostMessage(tid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
win32gui.PostMessage(tid, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
win32gui.SetForegroundWindow(tid)                           # 将窗口显示在最前
