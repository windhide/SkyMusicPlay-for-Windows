<template>
  <div id="father">
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      display: 'inline-block',
      color: 'black',
      background: '#F2C9C4',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <div style="flex-basis: 100%;" />
    <n-button type="primary" color="#f58f98" style="margin-top: 20px;" ghost @click="resetKeyToDefault()">
        {{ t("shortcutKeys.title") }}
    </n-button>
    <n-divider style="color: #F2C9C4;">{{ t("shortcutKeys.divider1") }}</n-divider>
    <div v-for="shortcut in musicShortcut" style="margin-right: auto;">
      <n-input-group style="margin-top: 20px">
        <n-button type="primary" text style="width: 100px;" color="#DDF2C4">
          {{ shortcut.name }}
        </n-button>
        <n-input v-model:value="shortcutKey['music_key'][shortcut.label]" readonly @blur="handleBlur()" placeholder=""
          @focus="handleFocus('music_key', shortcut.label)" />
      </n-input-group>
    </div>
    <n-divider style="color: #F2C9C4;">{{ t("shortcutKeys.divider2") }}</n-divider>
    <div v-for="shortcut in followShortcut" style="margin-right: auto;">
      <n-input-group style="margin-top: 20px">
        <n-button type="primary" text style="width: 100px;" color="#DDF2C4">
          {{ shortcut.name }}
        </n-button>
        <n-input v-model:value="shortcutKey['follow_key'][shortcut.label]" readonly @blur="handleBlur()" placeholder=""
          @focus="handleFocus('follow_key', shortcut.label)" />
      </n-input-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useThemeVars } from "naive-ui";
import { sendData } from "@renderer/utils/fetchUtils";
import { useMessage } from 'naive-ui'
import { onMounted, onUnmounted, ref } from 'vue'
import hotkeys from 'hotkeys-js';
import configStore, { CONFIG_TYPE } from '@renderer/utils/configStore'
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const themeVars = useThemeVars();
const message = useMessage()
const headText = t("shortcutKeys.head_text");
const patterns = [t("shortcutKeys.patterns1"),t("shortcutKeys.patterns2"),t("shortcutKeys.patterns3")];

const musicShortcut=[{ name: t("shortcutKeys.button_title.start"), label: "start",},{ name: t("shortcutKeys.button_title.resume"), label: "resume",},{ name: t("shortcutKeys.button_title.pause"), label: "pause",},{ name: t("shortcutKeys.button_title.stop"), label: "stop",},{ name: t("shortcutKeys.button_title.add_duration"), label: "add_duration"},{ name: t("shortcutKeys.button_title.reduce_duration"), label: "reduce_duration"},{ name: t("shortcutKeys.button_title.add_delay"), label: "add_delay"},{ name: t("shortcutKeys.button_title.reduce_delay"), label: "reduce_delay"},{ name: t("shortcutKeys.button_title.add_speed"), label: "add_speed"},{ name: t("shortcutKeys.button_title.reduce_speed"), label: "reduce_speed"},{ name: t("shortcutKeys.button_title.next"), label: "next",}]
const followShortcut=[{ name: t("shortcutKeys.button_title.repeat"), label: "repeat"},{ name: t("shortcutKeys.button_title.repeat_next"), label: "repeat_next"},{ name: t("shortcutKeys.button_title.exit"), label: "exit"},{ name: t("shortcutKeys.button_title.resize"), label: "resize"}]
const shortcutKey=ref({ follow_key:{ tap_key: "", string: "", repeat: "", repeat_next: "", resize: "", exit: ""}, music_key:{ next: "", pause: "", resume: "", start: "", stop: "", add_duration:"", reduce_duration: "", add_delay: "", reduce_delay:"", add_speed:"", reduce_speed:"", string: "",}})
const keyMapStruct={ "ScrollLock": "scroll_lock", "Escape": "esc", "PageUp": "page_up", "PageDown": "page_down", "ArrowUp": "up", "ArrowDown": "down", "ArrowLeft": "left", "ArrowRight": "right", "ControlRight": "ctrl_r", "AltRight": "alt_gr", "ControlLeft": "ctrl_l", "AltLeft": "alt_l", "ShiftLeft": "shift", "Enter": "enter", "Backspace": "backspace", "CapsLock": "caps_lock"}


function handleBlur() {
  hotkeys.unbind()
}

function handleFocus(type, label) {
  hotkeys('*', function (e) {
    console.log("e", e)

    let demoTranKey
    if (e.code in keyMapStruct) {
      demoTranKey = keyMapStruct[e.code].toUpperCase();
    } else if (e.code === "" && e.key === "Shift") {
      demoTranKey = "shift_r".toUpperCase()
    } else {
      demoTranKey = e.key.toUpperCase()
    }

    let tempStruct = JSON.parse(JSON.stringify(shortcutKey.value));
    tempStruct[type][label] = demoTranKey
    if (!checkDuplicates(tempStruct)) {
      message.error(t("setting.repeat"))
      return
    } else {
      shortcutKey.value[type][label] = demoTranKey
      configStore.setItem(CONFIG_TYPE.SHORTCUT_KEY, tempStruct)
      setShortcutKeys()
      message.success(t("setting.ok"))
    }
  })
}

function setShortcutKeys() {
  const shortcutKeyValues = shortcutKey.value;
  const follow = shortcutKeyValues.follow_key;
  const music = shortcutKeyValues.music_key;
  const followString = (follow.repeat + follow.repeat_next + follow.resize);
  const musicString = (music.next + music.pause + music.resume + music.start + music.stop + music.add_duration + music.reduce_duration + music.add_delay + music.reduce_delay + music.add_speed + music.reduce_speed);
  const followKey = {
    tap_key: "yuiophjkl;nm,./",
    repeat: follow.repeat.toLowerCase(),
    repeat_next: follow.repeat_next.toLowerCase(),
    resize: follow.resize.toLowerCase(),
    exit: follow.exit.toLowerCase(),
    // 使用计算后的字符串
    string: followString.toLowerCase()
  };
  const musicKey = {
    next: music.next.toLowerCase(),
    pause: music.pause.toLowerCase(),
    resume: music.resume.toLowerCase(),
    start: music.start.toLowerCase(),
    stop: music.stop.toLowerCase(),
    string: musicString.toLowerCase(),
    add_duration: music.add_duration.toLowerCase(),
    reduce_duration: music.reduce_duration.toLowerCase(),
    add_delay: music.add_delay.toLowerCase(),
    reduce_delay: music.reduce_delay.toLowerCase(),
    add_speed: music.add_speed.toLowerCase(),
    reduce_speed: music.reduce_speed.toLowerCase(),
  };
  sendData("config_operate", {
    "operate": "set",
    "name": "shortcutStruct",
    "value": {
      "follow_key": followKey,
      "music_key": musicKey
    }
  })
}
function getShortcutKeys() {
  return new Promise(resolve => {
    sendData("config_operate", {
      "operate": "get",
      "name": "shortcutStruct"
    }).then(res => {
      const follow = res.follow_key;
      const music = res.music_key;
      const followKey = {
        tap_key: follow.tap_key.toUpperCase(),
        repeat: follow.repeat.toUpperCase(),
        repeat_next: follow.repeat_next.toUpperCase(),
        resize: follow.resize.toUpperCase(),
        exit: follow.exit.toUpperCase(),
        string: follow.string.toUpperCase()
      };
      const musicKey = {
        next: music.next.toUpperCase(),
        pause: music.pause.toUpperCase(),
        resume: music.resume.toUpperCase(),
        start: music.start.toUpperCase(),
        stop: music.stop.toUpperCase(),
        add_duration: music.add_duration.toUpperCase(),
        reduce_duration: music.reduce_duration.toUpperCase(),
        add_delay: music.add_delay.toUpperCase(),
        reduce_delay: music.reduce_delay.toUpperCase(),
        add_speed: music.add_speed.toUpperCase(),
        reduce_speed: music.reduce_speed.toUpperCase(),
        string: music.string.toUpperCase()
      };
      shortcutKey.value.follow_key = followKey
      shortcutKey.value.music_key = musicKey
      resolve(true)
    })
  })
}

function checkDuplicates(shortcutObj) {
  const keys: any = [];
  for (const group in shortcutObj) {
    if (shortcutObj.hasOwnProperty(group)) {
      for (const key in shortcutObj[group]) {
        if (shortcutObj[group].hasOwnProperty(key) && key !== "string" && key !== "tap_key") {
          keys.push(shortcutObj[group][key]);
        }
      }
    }
  }
  const uniqueKeys = new Set(keys);
  return uniqueKeys.size === keys.length;
}
// 默认快捷方式
const defShortcutKey = {"follow_key":{"tap_key":"yuiophjkl;nm,./","string":"-=q","repeat":"-","repeat_next":'=',"resize":"q","exit":"esc"},"music_key":{"string":"f2f5f6f7f8updownleftrightpage_uppage_down","next":"f2","start":"f5","resume":"f6","pause":"f7","stop":"f8","add_duration":"up","reduce_duration":"down","add_delay":"right","reduce_delay":"left","add_speed":"page_up","reduce_speed":"page_down",}}
// 重置快捷方式
function resetKeyToDefault(){
  sendData("config_operate", {"operate":"set","name":"shortcutStruct","value": defShortcutKey
}).then(()=>{
    getShortcutKeys().then(() => {
      const tempStruct = JSON.parse(JSON.stringify(shortcutKey.value));
      configStore.setItem(CONFIG_TYPE.SHORTCUT_KEY, tempStruct)
    })
    message.success(t("setting.clearAll"))
  })
}

onMounted(() => {
  if(configStore.getItem(CONFIG_TYPE.SHORTCUT_KEY)){
    shortcutKey.value = configStore.getItem(CONFIG_TYPE.SHORTCUT_KEY)
    setShortcutKeys()
  }else{
    getShortcutKeys()
  }
})
onUnmounted(() => {
  hotkeys.unbind()
})
</script>

<style scoped>
#father {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

:deep(.n-slider-rail__fill) {
  --n-fill-color-hover: rgb(242, 232, 196) !important;
  background-color: rgb(242, 232, 196) !important;
}

:deep(.n-radio) {
  --n-box-shadow-active: inset 0 0 0 1px rgb(242, 232, 196) !important;
  --n-box-shadow-focus: inset 0 0 0 1px rgb(242, 232, 196), 0 0 0 2px rgba(242, 232, 196, 0.3) !important;
  --n-box-shadow-hover: inset 0 0 0 1px rgb(242, 232, 196) !important;
  --n-dot-color-active: rgb(242, 232, 196) !important;
}

:deep(.n-input) {
  --n-border-hover: 1px solid rgb(242, 232, 196) !important;
  --n-border-focus: 1px solid rgb(242, 232, 196) !important;
  --n-color-focus: rgba(242, 232, 196, 0.1) !important;
}
</style>
