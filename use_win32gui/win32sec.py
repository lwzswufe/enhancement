# author='lwz'
# coding:utf-8
import win32gui, win32con, win32api

window_ids = []
window_names = []


def get_window_name(hWnd, lparam):
    name = win32gui.GetWindowText(hWnd)
    # print(name)
    if win32gui.IsWindowVisible(hWnd) and len(name) > 0:
        print("hwnd: {} name: {}".format(hWnd, name))
        window_ids.append(hWnd)
        window_names.append(name)
        pass


def get_Class_name(handle, name, dhandle, d_data):
    name2 = win32gui.GetClassName(handle)
    print(name2)
    print(name)


win32gui.EnumWindows(get_window_name, None)
print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>")
window_name = ""
win = win32gui.FindWindow(None, window_name)
print("win:", win)
win32gui.EnumChildWindows(win, get_window_name, None)                           # 遍历子窗口
print("<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>")

for i, hwnd in enumerate(window_ids):                                           # 输出子窗口坐标
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    print("{}: {}-{}, {}-{}".format(window_names[i], left, right, top, bottom))

cw = 132122
left, top, right, bottom = win32gui.GetWindowRect(cw)                           # 获取窗口坐标

x = round((left + right) / 2)
y = round((bottom + top) / 2)

win32api.SetCursorPos([x, y])                                                   # 移动鼠标
print("x: ", x, "y:", y)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0 ,0 ,0 ,0)   # 鼠标点击 松开

print("x: ", x, "y:", y)
win32api.SetCursorPos([x, y])
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0 ,0 ,0 ,0)
win32api.keybd_event(52, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)                  # 按下数字4(52)
win32api.keybd_event(52, 0, win32con.KEYEVENTF_KEYUP, 0)                        # 松开数字4
y = 585
x = 330
print("x: ", x, "y:", y)
win32api.SetCursorPos([x, y])
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0 ,0 ,0 ,0)
win32api.keybd_event(49, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
win32api.keybd_event(49, 0, win32con.KEYEVENTF_KEYUP, 0)

win32api.keybd_event(48, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
win32api.keybd_event(48, 0, win32con.KEYEVENTF_KEYUP, 0)

win32api.keybd_event(48, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
win32api.keybd_event(48, 0, win32con.KEYEVENTF_KEYUP, 0)

win32api.keybd_event(48, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
win32api.keybd_event(48, 0, win32con.KEYEVENTF_KEYUP, 0)




