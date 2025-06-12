class GlobalVariable:
    # 运行环境配置
    isProd = False
    cpu_type = None
    compatibility_mode = False  # 是否虚拟机
    is_post_w = False  # 是否插队模式

    duration_prompt = """我想要你担任作曲家。我会提供一首歌的信息，然后你负责修改音乐。这可能需要使用各种乐器或工具，例如合成器或采样器，来创作旋律和和声，让歌词更加生动。所有对话和说明都应以中文提供。
这首歌的输入格式是一个 JSON 数组，每个元素如下：
{"time":0,"key":"1Key10","duration":400}
说明如下：
1. `time` 是音符的时间节点，单位毫秒。
2. `key` 是字符串，格式为 `{按键数}Key{音符编号}`，表示这个时间按下的音符。
   - 其中 key0代表C4，MIDI 60
   - key1代表D4，MIDI 62
   - key2代表E4，MIDI 64
   - key3代表F4，MIDI 65
   - key4代表G4，MIDI 67
   - key5代表A4，MIDI 69
   - key6代表B4，MIDI 71
   - key7代表C5，MIDI 72
   - key8代表D5，MIDI 74
   - key9代表E5，MIDI 76
   - key10代表F5，MIDI 77
   - key11代表G5，MIDI 79
   - key12代表A5，MIDI 81
   - key13代表B5，MIDI 83
   - key14代表C6，MIDI 84
3. `duration` 表示这个音要持续的时长（单位毫秒，最少 130 毫秒）。
🧠 **你需要做的事情：**
- 对输入内容进行改编，使旋律更生动自然。
- 添加或修改 `duration` 字段。
- 如果多个音符同时按下，使用相同的 `time` 和不同的 `key`。
- 保证输出是合法的 JSON 元素，结构完整：每个元素都必须是闭合的 `{"time":x,"key":"xKeyx","duration":x},`，不能出现半截。
- 每次输出最多 40 个 JSON 元素。
- 每次输出只包含数组中间部分，不要包含 `[` 或 `]`。
- 输出中的 key 必须严格是 `"time"`、`"key"`、`"duration"`，出现其他 key 直接忽略。
- **不要添加注释**。
- 不要输出文字说明，只输出 JSON 元素。
- 每次输出请在第一行注明：`第 N 段（共预计 M 段）`
- 当我回复“继续”时，你只输出**上一次的后续内容**，不要重复或重头输出。
⚠️ 最关键要求：
- 每次输出都是数组的一段，不能包含开头的 `[` 或结尾的 `]`；
- 每个对象结构必须闭合，不能有残缺；
- 输出完最后一段后，你可以提示我“已完成”。
🔽 请使用下面的数据进行改编：
{input}
"""
    translate_prompt = """你现在是一个音乐数据生成器，不是聊天助手。

🎼 输入是一首歌曲的音符数据，格式为一个 JSON 数组，每个元素如下：
{"time":0,"key":"1Key10"}

解释：
- `time` 表示时间，单位为毫秒。
- `key` 表示音符键名，格式为 `{轨道号}Key{音高编号}`。
- `轨道号` 是数字，如 `1` 或 `2`，表示旋律或和声的分轨。
- `音高编号` 必须从下表中选择：

| 编号 | keyN   | 对应音高        |
|------|--------|-----------------|
|  0   | Key0   | C4 (MIDI 60)    |
|  1   | Key1   | D4 (62)         |
|  2   | Key2   | E4 (64)         |
|  3   | Key3   | F4 (65)         |
|  4   | Key4   | G4 (67)         |
|  5   | Key5   | A4 (69)         |
|  6   | Key6   | B4 (71)         |
|  7   | Key7   | C5 (72)         |
|  8   | Key8   | D5 (74)         |
|  9   | Key9   | E5 (76)         |
| 10   | Key10  | F5 (77)         |
| 11   | Key11  | G5 (79)         |
| 12   | Key12  | A5 (81)         |
| 13   | Key13  | B5 (83)         |
| 14   | Key14  | C6 (84)         |

🧠 你的任务：
- 对原始旋律进行改编，使旋律更自然流畅。
- **允许自由发挥，增加音符数量不得少于原始音符总数，鼓励适度创新和变化。**
- 避免长时间重复相同旋律，保证整体音乐连贯性。
- 生成的 `time` 应合理反映节奏，避免毫秒级零散断裂，建议保持符合歌曲节拍风格。
- 轨道号代表不同声部，1号轨道为主旋律，2号轨道为和声伴奏，可适当调整和声层次。
- 同一时间点最多同时按下3个不同音符，保持和声自然。
- 每次输出最多 40 个完整 JSON 元素，不允许跨元素截断。
- 每个元素结构严格为：`{"time":1234,"key":"xKeyN"},`
- 所有 `key` 必须严格来自上方表格（含轨道前缀，如 `"1Key4"`）。
- 如果多个音符同时按下，使用相同的 `time` 和不同的 `key`。
- 允许对不合理音节进行改造，使其更符合音乐逻辑。

🧩 输出格式要求：
- 每次输出仅包含中间段 JSON 元素，不输出 `[` 或 `]`。
- 每次输出第一行必须注明：`第 N 段（共预计 M 段）`
- 输出不得包含除 JSON 结构外的任何注释、说明或总结语。
- 不得说“已完成”、“以下是输出”、“JSON 完整”等总结语。

🪛 响应规范：
- 保证每个 JSON 对象都闭合（不能残缺或中断）。
- 禁止输出非 `{"time":,"key":}` 格式的字段。
- 当我回复“继续”，你只输出**上一次后的 JSON 段落**，禁止重复。
- 你不能停止任务，除非我显式让你“停止”。

🎵 准备开始时，我会提供原始 JSON 数据，你必须根据以上规范对其改编并分段输出。

示例输出片段：
第 1 段（共预计 10 段）
{"time":0,"key":"1Key10"},{"time":250,"key":"1Key12"},{"time":250,"key":"2Key4"},{"time":500,"key":"1Key14"},
{"time":750,"key":"1Key13"},{"time":1000,"key":"1Key11"},{"time":1250,"key":"1Key9"},{"time":1250,"key":"2Key7"},
{"time":1500,"key":"1Key10"},{"time":1750,"key":"1Key12"}

"""
#     translate_prompt = """我想要你担任作曲家。我会提供一首歌的信息，然后你负责修改音乐。这可能需要使用各种乐器或工具，例如合成器或采样器，来创作旋律和和声，让歌词更加生动。所有对话和说明都应以中文提供。
# 这首歌的输入格式是一个 JSON 数组，每个元素如下：
# {"time":0,"key":"1Key10"}
# 说明如下：
# 1. `time` 是音符的时间节点，单位毫秒。
# 2. `key` 是字符串，格式为 `{按键数}Key{音符编号}`，表示这个时间按下的音符。
#    - 其中 key0代表C4，MIDI 60
#    - key1代表D4，MIDI 62
#    - key2代表E4，MIDI 64
#    - key3代表F4，MIDI 65
#    - key4代表G4，MIDI 67
#    - key5代表A4，MIDI 69
#    - key6代表B4，MIDI 71
#    - key7代表C5，MIDI 72
#    - key8代表D5，MIDI 74
#    - key9代表E5，MIDI 76
#    - key10代表F5，MIDI 77
#    - key11代表G5，MIDI 79
#    - key12代表A5，MIDI 81
#    - key13代表B5，MIDI 83
#    - key14代表C6，MIDI 84
# 🧠 **你需要做的事情：**
# - 对输入内容进行改编，使旋律更生动自然。
# - 如果多个音符同时按下，使用相同的 `time` 和不同的 `key`。
# - 保证输出是合法的 JSON 元素，结构完整：每个元素都必须是闭合的 `{"time":x,"key":"xKeyx"},`，不能出现半截。
# - 每次输出最多 40 个 JSON 元素。
# - 每次输出只包含数组中间部分，不要包含 `[` 或 `]`。
# - 输出中的 key 必须严格是 `"time"`、`"key"`，出现其他 key 直接忽略。
# - **不要添加注释**。
# - 不要输出文字说明，只输出 JSON 元素。
# - 每次输出请在第一行注明：`第 N 段（共预计 M 段）`
# - 当我回复“继续”时，你只输出**上一次的后续内容**，不要重复或重头输出。
# ⚠️ 最关键要求：
# - 每次输出都是数组的一段，不能包含开头的 `[` 或结尾的 `]`；
# - 每个对象结构必须闭合，不能有残缺；
# - 输出完最后一段后，你可以提示我“已完成”。
# 🔽 请使用下面的数据进行改编：
# {input}"""

    general_ai = {
    }

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
        "key_position": None,
        "wait": False
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
    now_total_time = ""
    now_current_time = ""

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
