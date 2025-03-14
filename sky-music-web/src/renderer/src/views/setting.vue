<template>
  <div id="headText">
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
        重 置 弹 琴 映 射
    </n-button>
    <n-divider style="color: #F2C9C4;">琴键映射</n-divider>
  </div>
  <div id="father">
    <div v-for="key in customize_key">
      <n-input-group style="margin-top: 20px">
        <n-button type="primary" text style="width: 15px;" color="#FF6347" v-if="key.name.includes('C') || key.name.includes('c')">
          {{ key.name }}
        </n-button>
        <n-button type="primary" text style="width: 15px;" color="#DDF2C4" v-else>
          {{ key.name }}
        </n-button>
        <n-input v-model:value="key.value" readonly clearable style="width: 71px;" placeholder="" @blur="handleBlur()" @focus="handleFocus(key.label)" @clear="handleClear(key.label)"	 />
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

const themeVars = useThemeVars();
const message = useMessage()
const customize_key:any = ref([])
const headText = "弹琴映射为本次运行生效，重启软件需要重新设置，如不适应请尽快适应";
const patterns = ["本次运行", "重新", "重启", "尽快适应"];
const keyMapStruct={ "ScrollLock": "scroll_lock", "Escape": "esc", "PageUp": "page_up", "PageDown": "page_down", "ArrowUp": "up", "ArrowDown": "down", "ArrowLeft": "left", "ArrowRight": "right", "ControlRight": "ctrl_r", "AltRight": "alt_gr", "ControlLeft": "ctrl_l", "AltLeft": "alt_l", "ShiftLeft": "shift", "Enter": "enter", "Backspace": "backspace", "CapsLock": "caps_lock"}

function handleBlur() {
  hotkeys.unbind()
}

function handleFocus(label) {
  hotkeys('*', function (e) {
    let demoTranKey
    if (e.code in keyMapStruct) {
      demoTranKey = keyMapStruct[e.code].toUpperCase();
    } else if (e.code === "" && e.key === "Shift") {
      demoTranKey = "shift_r".toUpperCase()
    } else {
      demoTranKey = e.key.toUpperCase()
    }
    
    let tempIndex = customize_key.value.findIndex(item => item.label === label);
    let tempArray = JSON.parse(JSON.stringify(customize_key.value))
    tempArray[tempIndex]["value"] = demoTranKey
    if (hasDuplicateValues(tempArray)) {
      message.error("存在重复的快捷键值，请检查配置。")
      return
    } else {
      customize_key.value[tempIndex]["value"] = demoTranKey
      set_customize_key()
      message.success("已设置")
    }
  })
}

function handleClear(label) {
    let tempIndex = customize_key.value.findIndex(item => item.label === label);
    customize_key.value[tempIndex]["value"] = ''
    set_customize_key()
    message.success("已清除本键")
}

function set_customize_key() {
  const transformedObject = {};
  customize_key.value.forEach(item => {
      transformedObject[item.label] = item.value.toLowerCase();
  });
  sendData("config_operate",{ "operate": "set", "name": "keyMap", "value":transformedObject}).then(()=>{
    get_customize_key()
  })
}

function get_customize_key() {
  sendData("config_operate", {
    "operate": "get",
    "name": "keyMap"
  }).then(res => {
    customize_key.value = [
    { "name": "C", "label": "Key-14", "value": res["Key-14"].toUpperCase()},
    { "name": "D", "label": "Key-13", "value": res["Key-13"].toUpperCase()},
    { "name": "E", "label": "Key-12", "value": res["Key-12"].toUpperCase()},
    { "name": "F", "label": "Key-11", "value": res["Key-11"].toUpperCase()},
    { "name": "G", "label": "Key-10", "value": res["Key-10"].toUpperCase()},
    { "name": "A", "label": "Key-9", "value": res["Key-9"].toUpperCase()},
    { "name": "B", "label": "Key-8", "value": res["Key-8"].toUpperCase()},
    { "name": "c", "label": "Key-7", "value": res["Key-7"].toUpperCase()},
    { "name": "d", "label": "Key-6", "value": res["Key-6"].toUpperCase()},
    { "name": "e", "label": "Key-5", "value": res["Key-5"].toUpperCase()},
    { "name": "f", "label": "Key-4", "value": res["Key-4"].toUpperCase()},
    { "name": "g", "label": "Key-3", "value": res["Key-3"].toUpperCase()},
    { "name": "a", "label": "Key-2", "value": res["Key-2"].toUpperCase()},
    { "name": "b", "label": "Key-1", "value": res["Key-1"].toUpperCase()},
    { "name": "c¹", "label": "Key0", "value": res["Key0"].toUpperCase()},
    { "name": "d¹", "label": "Key1", "value": res["Key1"].toUpperCase()},
    { "name": "e¹", "label": "Key2", "value": res["Key2"].toUpperCase()},
    { "name": "f¹", "label": "Key3", "value": res["Key3"].toUpperCase()},
    { "name": "g¹", "label": "Key4", "value": res["Key4"].toUpperCase()},
    { "name": "a¹", "label": "Key5", "value": res["Key5"].toUpperCase()},
    { "name": "b¹", "label": "Key6", "value": res["Key6"].toUpperCase()},
    { "name": "c²", "label": "Key7", "value": res["Key7"].toUpperCase()},
    { "name": "d²", "label": "Key8", "value": res["Key8"].toUpperCase()},
    { "name": "e²", "label": "Key9", "value": res["Key9"].toUpperCase()},
    { "name": "f²", "label": "Key10", "value": res["Key10"].toUpperCase()},
    { "name": "g²", "label": "Key11", "value": res["Key11"].toUpperCase()},
    { "name": "a²", "label": "Key12", "value": res["Key12"].toUpperCase()},
    { "name": "b²", "label": "Key13", "value": res["Key13"].toUpperCase()},
    { "name": "c³", "label": "Key14", "value": res["Key14"].toUpperCase()},
    { "name": "d³", "label": "Key15", "value": res["Key15"].toUpperCase()},
    { "name": "e³", "label": "Key16", "value": res["Key16"].toUpperCase()},
    { "name": "f³", "label": "Key17", "value": res["Key17"].toUpperCase()},
    { "name": "g³", "label": "Key18", "value": res["Key18"].toUpperCase()},
    { "name": "a³", "label": "Key19", "value": res["Key19"].toUpperCase()},
    { "name": "b³", "label": "Key20", "value": res["Key20"].toUpperCase()},
    { "name": "c⁴", "label": "Key21", "value": res["Key21"].toUpperCase()},
    { "name": "d⁴", "label": "Key22", "value": res["Key22"].toUpperCase()},
    { "name": "e⁴", "label": "Key23", "value": res["Key23"].toUpperCase()},
    { "name": "f⁴", "label": "Key24", "value": res["Key24"].toUpperCase()},
    { "name": "g⁴", "label": "Key25", "value": res["Key25"].toUpperCase()},
    { "name": "a⁴", "label": "Key26", "value": res["Key26"].toUpperCase()},
    { "name": "b⁴", "label": "Key27", "value": res["Key27"].toUpperCase()},
    { "name": "c⁵", "label": "Key28", "value": res["Key28"].toUpperCase()}]
  })
}

function hasDuplicateValues(dataArray) {
  const values = dataArray
    .filter(item => item.value !== undefined && item.value !== null && item.value !== '')
    .map(item => item.value);
  const uniqueValues = new Set(values);
  return uniqueValues.size !== values.length;
}

function resetKeyToDefault(){
  sendData("config_operate",{ "operate": "set", "name": "keyMap", "value":{ 'Key-14': '', 'Key-13': '', 'Key-12': '', 'Key-11': '', 'Key-10': '', 'Key-9': '', 'Key-8': '', 'Key-7': '', 'Key-6': '', 'Key-5': '', 'Key-4': '', 'Key-3': '', 'Key-2': '', 'Key-1': '', 'Key0': 'y', 'Key1': 'u', 'Key2': 'i', 'Key3': 'o', 'Key4': 'p', 'Key5': 'h', 'Key6': 'j', 'Key7': 'k', 'Key8': 'l', 'Key9': ';', 'Key10': 'n', 'Key11': 'm', 'Key12': ',', 'Key13': '.', 'Key14': '/', 'Key15': '', 'Key16': '', 'Key17': '', 'Key18': '', 'Key19': '', 'Key20': '', 'Key21': '', 'Key22': '', 'Key23': '', 'Key24': '', 'Key25': '', 'Key26': '', 'Key27': '', 'Key28': ''}}).then(()=>{
    get_customize_key()
    message.success("已重置快捷键")
  })
}

onMounted(() => {
  get_customize_key()
})
onUnmounted(() => {
  hotkeys.unbind()
})
</script>

<style scoped>
#headText {
  margin-top: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}
#father {
  display: flex;
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


:deep(.n-input){
  --n-border-hover: 1px solid rgb(242,232,196)!important;
  --n-border-focus: 1px solid rgb(242,232,196)!important;
  --n-caret-color: rgb(242,232,196)!important;
  --n-color-focus: rgba(242,232,196,0.1)!important;
}
</style>