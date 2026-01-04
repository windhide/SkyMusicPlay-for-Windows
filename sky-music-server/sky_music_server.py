import logging
import os
import queue
from contextlib import asynccontextmanager

import sys
import threading
import psutil
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sky_music_apis import register_routes
from windhide.static.global_variable import GlobalVariable
from windhide.thread.frame_alive_thread import monitor_process
from windhide.thread.hwnd_check_thread import start_thread as hwnd_check_thread
from windhide.thread.queue_thread import music_start_tasks
from windhide.thread.shortcut_thread import startThread as shortcut_thread
os.environ["TORCHAUDIO_USE_TORCHCODEC"] = "0"
# 设置 CPU 亲和性，避开与光遇相同核心运行
process = psutil.Process(os.getpid())
all_cores = list(range(psutil.cpu_count()))
# 避开光遇核心（假设是 0）和系统核心（可选避开 1）
available_cores = [core for core in all_cores if core not in [0, 1]]
# 选择前两个空闲核心
cores_to_use = available_cores[:2]
process.cpu_affinity(cores_to_use)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 检查是否为生产模式
    if "--prod" in sys.argv:
        GlobalVariable.isProd = True
    else:
        GlobalVariable.isProd = False
        print("当前为开发模式")

    # 启动快捷键监听线程
    shortcut_websocket_thread = threading.Thread(target=shortcut_thread, daemon=True)
    shortcut_websocket_thread.start()

    # 启动目标进程监控线程（仅在生产模式下）
    if GlobalVariable.isProd:
        target_process = "Sky_Music.exe"
        process_monitor_thread = threading.Thread(target=monitor_process, args=(target_process,), daemon=True)
        process_monitor_thread.start()

    # 启动窗口监听线程
    hwnd_thread = threading.Thread(target=hwnd_check_thread, daemon=True)
    hwnd_thread.start()

    # 初始化播放任务队列
    GlobalVariable.task_queue = queue.Queue()
    task_thread = threading.Thread(target=music_start_tasks, daemon=True)
    task_thread.start()
    yield  # 👈 此处之后 FastAPI 正式启动
    # 关闭时的清理逻辑（可选）
    print("应用正在关闭...")
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_routes(app)

if __name__ == '__main__':
    try:
        uvicorn.run(app, host="localhost", port=9899, log_config=None)
        logging.info("服务启动完成")
    except Exception as e:
        logging.error(e)