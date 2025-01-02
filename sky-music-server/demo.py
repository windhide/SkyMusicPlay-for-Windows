import time
import win32api
import win32con
import ctypes


# 模拟鼠标指针， 传送到指定坐标
# win32api.SetCursorPos([900, 300])
# 模拟鼠标点击
def left_mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)

# 键盘扫描码
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
# 模拟输入字母a
def key_down_and_up(num=0x41):  # 0x41是a
    # win32api.keybd_event(虚拟码，扫描码(游戏必填)，按下与抬起的标识，0）
    win32api.keybd_event(num, MapVirtualKey(num, 0), 0, 0)
    time.sleep(0.02)
    win32api.keybd_event(num, MapVirtualKey(num, 0), win32con.KEYEVENTF_KEYUP, 0)

if __name__ == '__main__':
    key_down_and_up(num=0x41)