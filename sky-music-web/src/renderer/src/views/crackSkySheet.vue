<template>
  <div id="headText">
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      color: 'black',
      background: '#F2C9C4',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText2" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      color: 'black',
      background: '#F2C9C4',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <n-divider style="color: #F2C9C4;">功能区</n-divider>
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText3" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      color: 'black',
      background: '#F2C9C4',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <div style="flex-basis: 100%;" />
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText4" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      color: 'black',
      background: '#F2C9C4',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <n-input-group style="margin-top: 20px ;width: 400px;">
      <n-button type="primary" text style="width: 90px;" color="#DDF2C4">
        歌曲名
      </n-button>
      <n-input v-model:value="songName" type="textarea" placeholder="歌曲名字/文件名字" style="flex-basis: 58%;"
        :autosize="{ minRows: 1, maxRows: 7 }" />
    </n-input-group>
    <n-input-group style="margin-top: 20px ;width: 400px;">
      <n-button type="primary" text style="width: 90px;" color="#DDF2C4">
        BPM
      </n-button>
      <n-input-number v-model:value="bpm" clearable style="width: 200px;"/>
    </n-input-group>
    <n-input-group style="margin-top: 20px ;width: 400px;">
      <n-button type="primary" text style="width: 90px;" color="#DDF2C4">
        检测间隔
      </n-button>
      <n-input-number v-model:value="interval" clearable style="width: 200px;"/>
    </n-input-group>
    <div style="flex-basis: 100%;" />
    <n-button type="primary" color="#f58f98" ghost @click="crack()" :loading="loading" style="margin-top: 30px ;width: 200px; margin-left: -20px;">
        开始破解
    </n-button>
  </div>
</template>

<script setup lang="ts">
import { useThemeVars } from "naive-ui";
import { sendData } from "@renderer/utils/fetchUtils";
import { ref } from 'vue'

const themeVars = useThemeVars();
const headText = "本软件解密功能专为乐谱创作者解决误加密问题设计，仅限合法使用。";
const headText2 = "用户需自行承担使用风险，开发者不承担任何法律责任。";
const headText3 = "1.要打开Sky Studio，并且进入里面选择被加密的谱子进入到Compose";
const headText4 = "2.输入Compose左边的BPM，即可开始";
const patterns = ["解密功能", "乐谱创作者", "创作者授权的情况", "合法", "自行承担使用风险","开发者不承担","打开Sky Studio", "进入到Compose", "BPM", "开始"];
const bpm = ref(200)
const interval = ref(0.05)
const songName = ref("")
const loading = ref(false)

function crack(){
  loading.value = true
  sendData("crack_skySheet",{
      "bpm":bpm.value,
      "interval":interval.value,
      "songName":songName.value
    }
  ).then(_res=>{
    loading.value = false
  })
}
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