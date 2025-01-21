import os
import time

from ultralytics import YOLO

from windhide.static.global_variable import GlobalVariable
from windhide.utils.ocr_normal_utils import get_window_screenshot
from windhide.utils.play_path_util import getResourcesPath, convert_notes_to_delayed_format

global_button_model = None


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
    image = get_window_screenshot()
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
            "height": height
        })
    result_dict = {}
    for box in all_boxes:
        y_key = box["top"]  # 使用上边距作为分组依据
        added = False
        for key in result_dict:
            if abs(key - y_key) <= threshold:  # 检查是否属于同一组
                result_dict[key].append(box)
                added = True
                break
        if not added:  # 如果没有匹配的组，创建新组
            result_dict[y_key] = [box]
    sorted_result = {}
    sorted_keys = sorted(result_dict)  # 按 y 坐标排序
    for idx, key in enumerate(sorted_keys):
        group = result_dict[key]
        group = sorted(group, key=lambda b: b["left"])
        avg_height = sum(b["height"] for b in group) / len(group)
        avg_width = sum(b["width"] for b in group) / len(group)
        if idx > 0:
            prev_key = sorted_keys[idx - 1]
            prev_bottom = max(b["bottom"] for b in result_dict[prev_key])  # 上一组的最大 bottom
            margin_top = key - prev_bottom
        else:
            margin_top = 0
        avg_margin_left = 0
        if len(group) > 1:
            margins = [group[i]["left"] - group[i - 1]["right"] for i in range(1, len(group))]
            avg_margin_left = sum(margins) / len(margins)
        sorted_result[key] = {
            "avg_height": avg_height,
            "avg_width": avg_width,
            "avg_margin_top": margin_top,
            "avg_margin_left": avg_margin_left
        }
    return sorted_result


def test_key_model_position(conf):
    time.sleep(1)
    image = get_window_screenshot()
    model = load_key_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    results[0].show()