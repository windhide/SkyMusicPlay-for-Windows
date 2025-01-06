isProd = False

thread = None
music_sheet = [] #乐谱
now_progress  = 0 #进度条
set_progress = -0.01 #进度条
# 音乐转换进度条
overall_progress = 0 #总体进度
tran_mid_progress = 0 # 转MID进度
now_translate_text = []
# 1秒 =1000毫秒
play_speed = 1 # 倍速
delay_interval = 0.01 # 10毫秒
sustain_time = 0.01 # 20毫秒
# 跟弹相关
follow_music = ""
follow_sheet = []
nowClientKey = ""
isNowAutoPlaying = False
isShow = False
nowRobotKey = ""
# 演奏核心
_hWnd = None
# 乐谱的映射
keyMap = {
    '1Key0':'y', '1Key1':'u', '1Key2':'i', '1Key3':'o', '1Key4':'p',
    '1Key5':'h', '1Key6':'j', '1Key7':'k', '1Key8':'l', '1Key9': ';',
    '1Key10':'n', '1Key11':'m', '1Key12':',', '1Key13':'.', '1Key14':'/',

    '2Key0': 'y', '2Key1': 'u', '2Key2': 'i', '2Key3': 'o', '2Key4': 'p',
    '2Key5': 'h', '2Key6': 'j', '2Key7': 'k', '2Key8': 'l', '2Key9': ';',
    '2Key10': 'n', '2Key11': 'm', '2Key12': ',', '2Key13': '.', '2Key14': '/',

    '3Key0': 'y', '3Key1': 'u', '3Key2': 'i', '3Key3': 'o', '3Key4': 'p',
    '3Key5': 'h', '3Key6': 'j', '3Key7': 'k', '3Key8': 'l', '3Key9': ';',
    '3Key10': 'n', '3Key11': 'm', '3Key12': ',', '3Key13': '.', '3Key14': '/',

    '4Key0': 'y', '4Key1': 'u', '4Key2': 'i', '4Key3': 'o', '4Key4': 'p',
    '4Key5': 'h', '4Key6': 'j', '4Key7': 'k', '4Key8': 'l', '4Key9': ';',
    '4Key10': 'n', '4Key11': 'm', '4Key12': ',', '4Key13': '.', '4Key14': '/',

    '5Key0': 'y', '5Key1': 'u', '5Key2': 'i', '5Key3': 'o', '5Key4': 'p',
    '5Key5': 'h', '5Key6': 'j', '5Key7': 'k', '5Key8': 'l', '5Key9': ';',
    '5Key10': 'n', '5Key11': 'm', '5Key12': ',', '5Key13': '.', '5Key14': '/',

    '6Key0': 'y', '6Key1': 'u', '6Key2': 'i', '6Key3': 'o', '6Key4': 'p',
    '6Key5': 'h', '6Key6': 'j', '6Key7': 'k', '6Key8': 'l', '6Key9': ';',
    '6Key10': 'n', '6Key11': 'm', '6Key12': ',', '6Key13': '.', '6Key14': '/',

    '7Key0': 'y', '7Key1': 'u', '7Key2': 'i', '7Key3': 'o', '7Key4': 'p',
    '7Key5': 'h', '7Key6': 'j', '7Key7': 'k', '7Key8': 'l', '7Key9': ';',
    '7Key10': 'n', '7Key11': 'm', '7Key12': ',', '7Key13': '.', '7Key14': '/',

    '8Key0': 'y', '8Key1': 'u', '8Key2': 'i', '8Key3': 'o', '8Key4': 'p',
    '8Key5': 'h', '8Key6': 'j', '8Key7': 'k', '8Key8': 'l', '8Key9': ';',
    '8Key10': 'n', '8Key11': 'm', '8Key12': ',', '8Key13': '.', '8Key14': '/',

    '9Key0': 'y', '9Key1': 'u', '9Key2': 'i', '9Key3': 'o', '9Key4': 'p',
    '9Key5': 'h', '9Key6': 'j', '9Key7': 'k', '9Key8': 'l', '9Key9': ';',
    '9Key10': 'n', '9Key11': 'm', '9Key12': ',', '9Key13': '.', '9Key14': '/',

    '10Key0': 'y', '10Key1': 'u', '10Key2': 'i', '10Key3': 'o', '10Key4': 'p',
    '10Key5': 'h', '10Key6': 'j', '10Key7': 'k', '10Key8': 'l', '10Key9': ';',
    '10Key10': 'n', '10Key11': 'm', '10Key12': ',', '10Key13': '.', '10Key14': '/',

    '11Key0': 'y', '11Key1': 'u', '11Key2': 'i', '11Key3': 'o', '11Key4': 'p',
    '11Key5': 'h', '11Key6': 'j', '11Key7': 'k', '11Key8': 'l', '11Key9': ';',
    '11Key10': 'n', '11Key11': 'm', '11Key12': ',', '11Key13': '.', '11Key14': '/',

    '12Key0': 'y', '12Key1': 'u', '12Key2': 'i', '12Key3': 'o', '12Key4': 'p',
    '12Key5': 'h', '12Key6': 'j', '12Key7': 'k', '12Key8': 'l', '12Key9': ';',
    '12Key10': 'n', '12Key11': 'm', '12Key12': ',', '12Key13': '.', '12Key14': '/',

    '13Key0': 'y', '13Key1': 'u', '13Key2': 'i', '13Key3': 'o', '13Key4': 'p',
    '13Key5': 'h', '13Key6': 'j', '13Key7': 'k', '13Key8': 'l', '13Key9': ';',
    '13Key10': 'n', '13Key11': 'm', '13Key12': ',', '13Key13': '.', '13Key14': '/',

    '14Key0': 'y', '14Key1': 'u', '14Key2': 'i', '14Key3': 'o', '14Key4': 'p',
    '14Key5': 'h', '14Key6': 'j', '14Key7': 'k', '14Key8': 'l', '14Key9': ';',
    '14Key10': 'n', '14Key11': 'm', '14Key12': ',', '14Key13': '.', '14Key14': '/',

    '15Key0': 'y', '15Key1': 'u', '15Key2': 'i', '15Key3': 'o', '15Key4': 'p',
    '15Key5': 'h', '15Key6': 'j', '15Key7': 'k', '15Key8': 'l', '15Key9': ';',
    '15Key10': 'n', '15Key11': 'm', '15Key12': ',', '15Key13': '.', '15Key14': '/'
}

vk_code_map = {
    # 数字键
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,

    # 字母键
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
    'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
    'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F,
    'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
    'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59,
    'Z': 0x5A,

    # 功能键
    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
    'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77,
    'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,

    # 控制键
    'ESC': 0x1B, 'TAB': 0x09, 'CAPSLOCK': 0x14, 'SHIFT': 0x10,
    'CTRL': 0x11, 'ALT': 0x12, 'SPACE': 0x20, 'ENTER': 0x0D,
    'BACKSPACE': 0x08, 'DELETE': 0x2E, 'INSERT': 0x2D,
    'HOME': 0x24, 'END': 0x23, 'PAGEUP': 0x21, 'PAGEDOWN': 0x22,

    # 箭头键
    'LEFT': 0x25, 'UP': 0x26, 'RIGHT': 0x27, 'DOWN': 0x28,

    # 数字小键盘
    'NUM0': 0x60, 'NUM1': 0x61, 'NUM2': 0x62, 'NUM3': 0x63,
    'NUM4': 0x64, 'NUM5': 0x65, 'NUM6': 0x66, 'NUM7': 0x67,
    'NUM8': 0x68, 'NUM9': 0x69,
    'NUMLOCK': 0x90, 'DIVIDE': 0x6F, 'MULTIPLY': 0x6A,
    'SUBTRACT': 0x6D, 'ADD': 0x6B, 'DECIMAL': 0x6E,

    # 符号键
    ';': 0xBA, '=': 0xBB, ',': 0xBC, '-': 0xBD, '.': 0xBE,
    '/': 0xBF, '`': 0xC0, '[': 0xDB, '\\': 0xDC, ']': 0xDD,
    "'": 0xDE,

    # Windows 键
    'LWIN': 0x5B, 'RWIN': 0x5C, 'APPS': 0x5D,

    # 媒体控制键
    'VOLUME_MUTE': 0xAD, 'VOLUME_DOWN': 0xAE, 'VOLUME_UP': 0xAF,
    'MEDIA_NEXT_TRACK': 0xB0, 'MEDIA_PREV_TRACK': 0xB1,
    'MEDIA_STOP': 0xB2, 'MEDIA_PLAY_PAUSE': 0xB3,

    # 其他
    'PRINTSCREEN': 0x2C, 'SCROLLLOCK': 0x91, 'PAUSE': 0x13,
    'NUMENTER': 0x0D,  # 小键盘上的 ENTER 键
}