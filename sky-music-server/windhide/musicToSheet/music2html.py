import os

from jinja2 import Template
from platformdirs import user_desktop_dir

html_template = """
<!DOCTYPE html>
<html lang="en_US">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<title>{{ sheet_name }}</title>
		<style type="text/css">
@media (prefers-reduced-motion: reduce){html { scroll-behavior: auto; }}
html { scroll-behavior: smooth; }
#navigation { border: none; }
#transcript { margin: 0 0; }
body{font-family: "Noto Sans", "Noto Sans CJK JP", "Noto Sans CJK KR", "Noto Sans CJK SC", "Noto Sans CJK TC", "Avenir", "Arial", "sans-serif";font-size: 12pt;}
h1{font-size: 1.3em;font-weight: bold;}
.header{font-size: 0.8em;line-height: 50%;}
.line{display: flex;flex-direction: row;flex-wrap: wrap;}
.lyrics{margin-left: 0.5rem;margin-bottom: 0.35rem;border: 0px black solid;width: 8.11em;font-size: 0.8em;text-align: center;}
hr{border: none;margin-left: 0;padding: 0;margin-right: 1.8em;width: 100vw;}
hr.sep { border-top: thin solid lightgray; width: 93vw; }
hr.solid { border-top: thin solid black; }
hr.double { border-top: medium double black; }
hr.dashed { border-top: thin dashed black; }
.instr.silent, .instr.broken{border-width: 0;background-color: transparent;}
.repeat, .num{font-size: 0.8em;align-self: flex-end;margin: 2px;}
.num{color: grey;padding-left: 2em;}
.broken{color: red;font-weight: bold;}
@media (prefers-color-scheme: dark){body { background-color: #282828; }.instr.harp { border-color: white; }p, body, td, text.headers { color: white; }}
.instr{margin-left: 0.5rem;margin-bottom: 0.35rem;border-radius: 5px;border: 1px black solid;display: grid;width: fit-content;}
.instr.harp {grid-template-columns: repeat(5, 1.3em); grid-template-rows: repeat(3, 1.4em);}
.instr.drum {grid-template-columns: repeat(4, 1.3em); grid-template-rows: repeat(2, 1.4em);}
.r1, .r2, .r3, [class^="q"]{border-radius: 4px;margin: 2px;width: 1em;height: 1em;justify-self: center;align-self: center;}
d1, d2, d3, silence { background-position: 50%; }
.r1 { background-color: limegreen; }
.r2 { background-color: deepskyblue; }
.r3 { background-color: deeppink; }
crc { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 91 91'%3E%3Ccircle fill='transparent' stroke='white' stroke-width='5px' cx='45.4' cy='45.4' r='25.5'%3E%3C/circle%3E%3C/svg%3E"); }
dmn { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 123.40601 123.40601'%0A%3E%3Cg transform='translate(-52.444184,-69.21989)'%0A%3E%3Crect style='fill:none;stroke:white ;stroke-width:5px;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:100;stroke-dasharray:none;' width='64.633926' height='64.633926' x='140.97375' y='-20.454748' transform='rotate(45)' /%3E%3C/g%3E%3C/svg%3E"); }
crdm { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 123.40601 123.40601'%0A%3E%3Cg transform='translate(-52.444184,-69.21989)' %3E%3Crect style='fill:none;stroke:white;stroke-width:5px;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1' width='64.633926' height='64.633926' x='140.97375' y='-20.454748' transform='rotate(45)' /%3E%3Ccircle style='fill:none;stroke:white;stroke-width:5px;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1' cx='114.12409' cy='130.82843' r='31.938707' /%3E%3C/g%3E%3C/svg%3E"); }
d1 { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 123.40601 123.40601'%3E%3Ccircle stroke='none' fill='rgb(194,240,194)' cx='61.5' cy='61.5' r='14'%3E%3C/circle%3E%3C/svg%3E"); }
d2 { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 123.40601 123.40601'%3E%3Ccircle stroke='none' fill='rgb(179,236,255)' cx='61.5' cy='61.5' r='14'%3E%3C/circle%3E%3C/svg%3E"); }
d3 { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 123.40601 123.40601'%3E%3Ccircle stroke='none' fill='rgb(255,185,223)' cx='61.5' cy='61.5' r='14'%3E%3C/circle%3E%3C/svg%3E"); }
dn { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 123.40601 123.40601'%3E%3Ccircle stroke='none' fill='rgb(167,167,167)' cx='61.5' cy='61.5' r='14'%3E%3C/circle%3E%3C/svg%3E"); }
silence { background-image: url("data:image/svg+xml, %3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 123.40601 123.40601'%3E%3Ccircle stroke='none' fill='rgb(167,167,167)' cx='61.5' cy='61.5' r='28'%3E%3C/circle%3E%3C/svg%3E"); }
</style></head>
<body>
<h1>{{ sheet_name }}</h1>
<p class="header"><b>文件由：WindHide's Sky Music弹琴软件创建</b> <a href="https://github.com/windhide/SkyMusicPlay-for-Windows" style="color: pink;">https://github.com/windhide/SkyMusicPlay-for-Windows</a></p>
<p class="header"><b></b></p>
</div>
<div id="transcript">
    {% for line in content %}
    <hr class="sep">
    <div class="line" id="{{ line.id }}">
        {% for instr in line.instruments %}
        <div class="instr harp" id="{{ instr.id }}">
            {% for note in instr.notes %}
            <{{ note.type }} class="{{ note.class }}"></{{ note.type }}>
            {% endfor %}
        </div>
        {% endfor %}
    </div>
    {% endfor %}
</div>
</body></html>
"""


def generatorSheetHtml(sheet_name, convert_sheet):
    context = []
    instr_index = 0
    line_index = 0
    line_data = {"id": f"line-{line_index}", "instruments": []}

    max_instruments_per_line = 13
    switch_limit = {13: 11, 11: 13}  # 交替限制

    # 映射按键到音符类型
    note_mapping = {
        "y": ("crdm", "r1"),
        "u": ("dmn", "r1"),
        "i": ("crc", "r1"),
        "o": ("dmn", "r1"),
        "p": ("crc", "r1"),

        "h": ("crc", "r2"),
        "j": ("dmn", "r2"),
        "k": ("crdm", "r2"),
        "l": ("dmn", "r2"),
        ";": ("crc", "r2"),

        "n": ("crc", "r3"),
        "m": ("dmn", "r3"),
        ",": ("crc", "r3"),
        ".": ("dmn", "r3"),
        "/": ("crdm", "r3"),
    }

    for index, key in enumerate(convert_sheet):
        notes = []
        for char in "yuiophjkl;nm,./":
            if char in key:
                note_type, note_class = note_mapping[char]
            else:
                note_type, note_class = "d1", ""  # 默认值

            notes.append({"type": note_type, "class": note_class})

        instrument = {"id": f"instr-{instr_index}", "notes": notes}
        line_data["instruments"].append(instrument)
        instr_index += 1

        # 判断是否换行
        if instr_index == max_instruments_per_line:
            context.append(line_data)
            line_index += 1
            line_data = {"id": f"line-{line_index}", "instruments": []}
            instr_index = 0
            max_instruments_per_line = switch_limit[max_instruments_per_line]

    # 处理最后一行
    if line_data["instruments"]:
        context.append(line_data)

    # 渲染模板
    template = Template(html_template)
    final_html = template.render(sheet_name=sheet_name, content=context)

    desktop_path = os.path.join(user_desktop_dir(), f"{sheet_name}.html")
    with open(desktop_path, "w", encoding="utf-8") as file:
        file.write(final_html)

    return "ok"
