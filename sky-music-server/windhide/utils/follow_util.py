from windhide._global import global_variable
from windhide.utils.music_file_transelate import convert_notes_to_delayed_format


def set_next_sheet(request: dict):
    try:
        print(f"Setting follow sheet for file: {request['fileName']}")
        convert_notes_to_delayed_format(request["fileName"], request["type"])
        global_variable.follow_sheet = list(map(lambda item: item['key'], global_variable.music_sheet))
        global_variable.music_sheet = []
        global_variable.follow_music = request["fileName"]
    except Exception as e:
        print(f"Error in /followSheet: {str(e)}")


def get_next_sheet(request: dict):
    if len(global_variable.follow_sheet) == 0:
        return ""
    try:
        if request["type"] == "ok":
            sheet = global_variable.follow_sheet[0]
            global_variable.nowClientKey = sheet
            global_variable.follow_sheet = global_variable.follow_sheet[1:]
            return sheet
        else:
            global_variable.nowClientKey = global_variable.follow_sheet[0]
            return global_variable.follow_sheet[0]
    except IndexError:
        print("空数组")
        return ""
