class GlobalVariable:
    # 运行环境配置
    isProd = False
    cpu_type = None
    compatibility_mode = False  # 是否虚拟机
    is_post_w = False  # 是否插队模式

    # 窗口相关
    is_custom_hwnd = False
    hwnd_title = "Sky.exe"
    hwnd_select_struct = {}
    window = {
        "hWnd": None,
        "width": 0,
        "height": 0,
        "position_x": 0,
        "position_y": 0,
        "is_change": False,
        "key_position": None
    }

    # 快捷键相关
    shortcutStruct = {
        "follow_key":{
            "tap_key": "yuiophjkl;nm,./",
            "string": "-=q",
            "repeat": "-",
            "repeat_next": '=',
            "resize": "q",
            "exit": "esc"
        },
        "music_key":{
            "string": "f2f5f6f7f8updownleftrightpage_uppage_down",
            "next": "f2",
            "start": "f5",
            "resume": "f6",
            "pause": "f7",
            "stop": "f8",
            "add_duration": "up",
            "reduce_duration": "down",
            "add_delay": "right",
            "reduce_delay": "left",
            "add_speed": "page_up",
            "reduce_speed": "page_down",
        }
    }
    # 线程相关
    thread = None
    auto_thread = None
    task_queue = None

    # 乐谱相关
    music_sheet = []  # 乐谱

    # 进度条相关
    now_progress = 0  # 进度条
    set_progress = -0.01  # 进度条
    now_play_music = "没有正在播放的歌曲哦"

    # 音乐转换进度条
    overall_progress = 0  # 总体进度
    now_translate_text = []
    merge_min = 20
    merge_max = 30
    velocity_filter = 10
    is_singular = True
    semitone_switch = True # 半音转换开关
    detail_switch = True # 超3音转换开关

    # 演奏相关
    play_speed = 1  # 倍速
    delay_interval = 0  # 0
    duration = 0  # 20毫秒

    # 跟弹相关
    follow_music = ""
    follow_sheet = []
    nowClientKey = ""
    nowRobotKey = ""
    follow_client = None
    isNowAutoPlaying = False
    follow_thread = None  # 跟弹按键处理相关线程
    exit_flag = False
    draw_process = None
    window_offset_x = 0
    window_offset_y = 0
    follow_process = None

    # 乐谱映射
    keyMap = {
        'Key-14': '', 'Key-13': '', 'Key-12': '', 'Key-11': '', 'Key-10': '', 'Key-9': '', 'Key-8': '',
        'Key-7': '', 'Key-6': '', 'Key-5': '', 'Key-4': '', 'Key-3': '', 'Key-2': '', 'Key-1': '',
        'Key0': 'y', 'Key1': 'u', 'Key2': 'i', 'Key3': 'o', 'Key4': 'p', 'Key5': 'h', 'Key6': 'j',
        'Key7': 'k', 'Key8': 'l', 'Key9': ';', 'Key10': 'n', 'Key11': 'm', 'Key12': ',', 'Key13': '.',
        'Key14': '/', 'Key15': '', 'Key16': '', 'Key17': '', 'Key18': '', 'Key19': '', 'Key20': '',
        'Key21': '', 'Key22': '', 'Key23': '', 'Key24': '', 'Key25': '', 'Key26': '', 'Key27': '',
        'Key28': ''
    }
