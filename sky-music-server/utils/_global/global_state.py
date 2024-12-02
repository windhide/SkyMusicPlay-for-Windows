windows_name = ""
window_activated = False
target_window = None
play_state = 'play' # play pause stop
thread = None
music_sheet = [] #乐谱
now_progress  = 0 #进度条
set_progress = -0.01 #进度条
# 音乐转换进度条
overall_progress = 0 #总体进度
tran_mid_progress = 0 # 转MID进度
# MID转TXT进度
now_translate_text = []
# 延迟毫秒
delay_interval = 0.002
sustain_time = 0