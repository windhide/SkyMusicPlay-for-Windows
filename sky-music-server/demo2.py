import win32api
import win32gui
from ctypes import windll
import win32con

def clickLeftCur():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def leftDown(pos, hd):
    handle = hd
    client_pos = win32gui.ScreenToClient(handle, pos)
    tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)

def leftUp(pos, hd):
    handle = hd
    client_pos = win32gui.ScreenToClient(handle, pos)
    tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)

def click_it(pos, hd):
    handle = hd
    # moveCurPos(pos[0], pos[1])
    client_pos = win32gui.ScreenToClient(handle, pos)
    tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)

def click_it_a(pos, hd):
    handle = hd
    client_pos = win32gui.ScreenToClient(handle, pos)
    tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
    win32gui.PostMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.PostMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
    win32gui.PostMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)

def moveCurPos(x, y):  # 移动鼠标
    windll.user32.SetCursorPos(x, y)


def getCurPos():  # 获得鼠标位置信息，这个再实际代码没用上，调试用得上
    return win32gui.GetCursorPos()

def dragCur(param, hd):
    leftDown((param[0], param[1]), hd)
    leftUp((param[0], param[1]), hd)
