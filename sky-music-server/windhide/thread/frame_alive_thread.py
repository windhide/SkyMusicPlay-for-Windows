import os
import time

import psutil


def is_process_running(process_name):
    """检查目标进程是否运行"""
    return any(proc.info["name"] == process_name for proc in psutil.process_iter(["name"]))


def monitor_process(process_name):
    """监听目标进程的状态，如果退出则结束主程序"""
    print(f"🔍 监听进程: {process_name}")
    while True:
        if not is_process_running(process_name):
            print(f"⚠️ {process_name} 已退出，关闭主程序。")
            os._exit(0)  # 强制退出主进程
        time.sleep(1)  # 每秒检查一次
