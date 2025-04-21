import logging
import os
import threading
import time

from ultralytics import YOLO

from windhide.static.global_variable import GlobalVariable
from windhide.thread.follow_thread import startThread as follow_thread_demo
from windhide.utils.command_util import start_process
from windhide.utils.ocr_normal_utils import get_window_screenshot
from windhide.utils.path_util import getResourcesPath, convert_notes_to_delayed_format

global_button_model = None

logging.getLogger("ultralytics").setLevel(logging.WARNING)

def set_next_sheet(request: dict):
    try:
        print(f"Setting follow sheet for file: {request['fileName']}")
        convert_notes_to_delayed_format(request["fileName"], request["type"])
        GlobalVariable.follow_sheet = list(map(lambda item: item['key'], GlobalVariable.music_sheet))
        GlobalVariable.music_sheet = []
        GlobalVariable.follow_music = request["fileName"]
    except Exception as e:
        print(f"Error in /followSheet: {str(e)}")


def get_next_sheet(request: dict):
    if len(GlobalVariable.follow_sheet) == 0:
        return ""
    try:
        if request["type"] == "ok":
            sheet = GlobalVariable.follow_sheet[0]
            GlobalVariable.nowClientKey = sheet
            GlobalVariable.follow_sheet = GlobalVariable.follow_sheet[1:]
            return sheet
        else:
            GlobalVariable.nowClientKey = GlobalVariable.follow_sheet[0]
            return GlobalVariable.follow_sheet[0]
    except IndexError:
        print("空数组")
        return ""

def load_key_model():
    """加载模型并保存在全局变量中"""
    global global_button_model
    if global_button_model is None:
        button_model_path = os.path.join(getResourcesPath("systemTools"), "modelData", "check_key_model.pt")
        global_button_model = YOLO(button_model_path)  # 加载模型并保存在 global_friend_model 中
        print("模型加载完成")
    return global_button_model


def get_key_position(conf, threshold=10):
    if GlobalVariable.window["key_position"] is not None:
        if len(GlobalVariable.window["key_position"]) == 15 and not GlobalVariable.window["is_change"]:
            return GlobalVariable.window["key_position"]
    print("开始检测按键布局")
    GlobalVariable.window["key_position"] = None
    image = None
    try:
        bgr_image = get_window_screenshot()
        height, width = bgr_image.shape[:2]
        crop_width = int(width * 0.15)  # 右边10%的宽度
        crop_height = int(height * 0.1)  # 底部 10% 的高度
        image = bgr_image[: -crop_height, : -crop_width]
    except Exception as e:
        print(e)

    model = load_key_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    boxes = results[0].boxes  # 检测到的所有框
    xyxy = boxes.xyxy.cpu().numpy()  # 获取每个框的绝对坐标 (x1, y1, x2, y2)
    all_boxes = []
    for box in xyxy:
        x1, y1, x2, y2 = box
        width = int(x2 - x1)
        height = int(y2 - y1)
        all_boxes.append({
            "left": int(x1),
            "top": int(y1),
            "right": int(x2),
            "bottom": int(y2),
            "width": width,
            "height": height,
            "position_x": int(x1),  # 添加 position_x
            "position_y": int(y1)  # 添加 position_y
        })
    result_dict = {}
    for box in all_boxes:
        y_key = box["top"]  # 使用上边距作为分组依据
        added = False
        for key in result_dict:
            if abs(key - y_key) <= threshold:
                result_dict[key].append(box)
                added = True
                break
        if not added:
            result_dict[y_key] = [box]
    sorted_result = {}
    sorted_keys = sorted(result_dict)
    for key in sorted_keys:
        group = result_dict[key]
        sorted_group = sorted(group, key=lambda b: b["position_x"])
        sorted_result[key] = [{
            "width": box["width"],
            "height": box["height"],
            "position_x": box["position_x"],
            "position_y": box["position_y"]
        } for box in sorted_group]
    key_mapping = {
        0: ["y", "u", "i", "o", "p"],  # 第一组
        1: ["h", "j", "k", "l", ";"],  # 第二组
        2: ["n", "m", ",", ".", "/"]  # 第三组
    }
    final_result = {}
    for idx, (group_key, group_boxes) in enumerate(zip(sorted_keys, sorted_result.values())):
        if idx == 3:
            break
        # 避免越界
        keys = key_mapping[idx]  # 获取当前分组的键名列表
        for key_name, box in zip(keys, group_boxes):
            final_result[key_name] = box  # 使用键名作为最终结果的 key
    GlobalVariable.window["key_position"] = final_result
    if len(final_result) == 15:
        GlobalVariable.window["is_change"] = False
        GlobalVariable.window["wait"] = False
    return final_result

def test_key_model_position(conf):
    image = None
    time.sleep(1)
    try:
        bgr_image = get_window_screenshot()
        height, width = bgr_image.shape[:2]
        crop_width = int(width * 0.15)  # 右边10%的宽度
        crop_height = int(height * 0.1)  # 底部 10% 的高度
        image = bgr_image[: -crop_height, : -crop_width]
    except Exception as e:
        print(e)
    model = load_key_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    results[0].show()

def open_follow():
    start_process()
    GlobalVariable.follow_thread = threading.Thread(target=follow_thread_demo)
    GlobalVariable.follow_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    GlobalVariable.follow_thread.start()
