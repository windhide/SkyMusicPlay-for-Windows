thread = None
music_sheet = [] #乐谱
now_progress  = 0 #进度条
set_progress = -0.01 #进度条
# 音乐转换进度条
overall_progress = 0 #总体进度
tran_mid_progress = 0 # 转MID进度
# MID转TXT进度
now_translate_text = []
# 1秒 =1000毫秒
play_speed = 1 # 倍速
delay_interval = 0.01 # 10毫秒
sustain_time = 0.01 # 20毫秒
follow_music = ""
follow_sheet = []