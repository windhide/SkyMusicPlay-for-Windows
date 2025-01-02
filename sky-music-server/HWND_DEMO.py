import win32gui


hwnd_title = dict()

def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

def get():
    list = []
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t != "":
            # if t == '夜神模拟器':
            if t == '阴阳师-网易游戏':
                list.append(h)
                print(h)
    return list

if __name__ == '__main__':
    get()