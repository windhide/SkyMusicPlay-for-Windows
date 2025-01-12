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
    # tempfile
    # data = {
    #     "sheet_name": sheet_name,
    #     "content": [
    #         {
    #             "id": "line-0",
    #             "instruments": [
    #                 {
    #                     "id": "instr-0",
    #                     "notes": [
    #                         {"type": "d1", "class": "r1"},
    #                         {"type": "dmn", "class": "r1"},
    #                         {"type": "d1", "class": ""}
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }

    context = []
    instrIndex = 0
    lineIndex = 0
    instruments = []
    struct = {
        "id": f"line-{lineIndex}",
        "instruments": []
    }
    indexChangeLine = 13
    for index, key in enumerate(convert_sheet):
        instrument = {
            "id": f"instr-{instrIndex}",
            "notes": [
                {"type": "crdm" if 'y' in key else "d1", "class": "r1" if 'y' in key else ""},
                {"type": "dmn" if 'u' in key else "d1", "class": "r1" if 'u' in key else ""},
                {"type": "crc" if 'i' in key else "d1", "class": "r1" if 'i' in key else ""},
                {"type": "dmn" if 'o' in key else "d1", "class": "r1" if 'o' in key else ""},
                {"type": "crc" if 'p' in key else "d1", "class": "r1" if 'p' in key else ""},

                {"type": "crc" if 'h' in key else "d2", "class": "r2" if 'h' in key else ""},
                {"type": "dmn" if 'j' in key else "d2", "class": "r2" if 'j' in key else ""},
                {"type": "crdm" if 'k' in key else "d2", "class": "r2" if 'k' in key else ""},
                {"type": "dmn" if 'l' in key else "d2", "class": "r2" if 'l' in key else ""},
                {"type": "crc" if ';' in key else "d2", "class": "r2" if ';' in key else ""},

                {"type": "crc" if 'n' in key else "d3", "class": "r3" if 'n' in key else ""},
                {"type": "dmn" if 'm' in key else "d3", "class": "r3" if 'm' in key else ""},
                {"type": "crc" if ',' in key else "d3", "class": "r3" if ',' in key else ""},
                {"type": "dmn" if '.' in key else "d3", "class": "r3" if '.' in key else ""},
                {"type": "crdm" if '/' in key else "d3", "class": "r3" if '/' in key else ""}
            ]
        }
        instrIndex += 1
        struct["instruments"].append(instrument)
        if instrIndex == indexChangeLine:
            if indexChangeLine == 13:
                indexChangeLine = 11
            else:
                indexChangeLine = 13
            instrIndex = 0
            instruments.append(struct)
            lineIndex += 1
            context.append(struct)
            struct = {
                "id": f"line-{lineIndex}",
                "instruments": []
            }

    data = {"sheet_name": sheet_name, "content": context}
    # 渲染模板
    template = Template(html_template)
    final_html = template.render(data)
    desktop_path = os.path.join(user_desktop_dir(), f"{sheet_name}.html")
    print(desktop_path)
    with open(desktop_path, "w", encoding="utf-8") as file:
        file.write(final_html)
    return "ok"
