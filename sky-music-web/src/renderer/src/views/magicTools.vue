<template>
  <div class="father">
    <n-divider>
        ⚠
    </n-divider>
    <div class="father">
      <n-highlight style="margin-bottom: 5px" :text="headText" :patterns="patterns" :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2E8C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }" />
      <n-highlight style="margin-bottom: 5px" :text="headText2" :patterns="patterns" :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2E8C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }" />
      <n-highlight style="margin-bottom: 5px" :text="headText3" :patterns="patterns" :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2E8C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }" />
      <n-divider />
      <div class="father">
        <n-space style="width: 100%;" align='center' justify='center'>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('Y')">Y</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('U')">U</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('I')">I</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('O')">O</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('P')">P</n-button>
        </n-space>
        <n-space class="dynamicSpaceStyles" align='center' justify='center'>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('H')">H</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('J')">J</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('K')">K</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('L')">L</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress(';')">;</n-button>
        </n-space>
        <n-space class="dynamicSpaceStyles" align='center' justify='center'>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('N')">N</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('M')">M</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress(',')">,</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('.')">.</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('/')">/</n-button>
        </n-space>
      </div>
      <n-divider />
      <div style="flex: 0 0 100%;" class="father">
        <n-button type="warning" ghost @click="autoClickFire">
          自动点火（站在星盘上，确保游戏出现了按钮G快捷键，再点本按钮）
        </n-button>
      </div>
      <div class="father" v-for="button in buttons">
        <n-button dashed :color=button.color @click="run(button.value)"
          :style="{ marginTop: '20px', marginLeft: button.value === 'all' ? '0' : '15px' }"
          v-if="button.value != 'developer'">
          {{ button.context }}
        </n-button>
        <n-upload v-else action="http://localhost:9899/autoScriptUpload" style="margin-top:20px; margin-left: 15px;" accept=".txt"
          :show-file-list="false">
          <n-button type="info" dashed :color=button.color> {{ button.context }}</n-button>
        </n-upload>
      </div>
      <div style="width:100%" />
      <n-select v-model:value="selectValue" :options="options" style="width: 15%; margin-top: 20px;" />
        <n-input-number v-model:value="mathValue" clearable step="0.01" style="margin-top: 20px; margin-left: 20px;" />
        <n-button type="error" dashed style="margin-left: 20px;margin-top: 20px;" @click="checkFile">
          Check
        </n-button>
    </div>
    
  </div>
</template>

<script setup lang="ts">
import { sendData } from "@renderer/utils/fetchUtils";
import { useThemeVars } from "naive-ui";
import { ref } from "vue";
const themeVars = useThemeVars();
const headText = "此处是测试版功能请谨慎使用🌶，不涉及内存修改🌶。";
const headText2 = "此处功能仅供学习交流，严禁用于商业用途，请于24小时内删除";
const headText3 = "🚫模拟器玩家禁止使用下面的所有功能🚫";
const patterns = ["谨慎使用🌶", "不涉及内存修改🌶", "此处功能仅供学习交流，严禁用于商业用途，请于24小时内删除", "🚫模拟器玩家禁止使用下面的所有功能🚫"];
let mathValue = ref(0.5)
let selectValue = ref("image")
const options = [
  {
    label: '心火',
    value: 'image'
  },
  {
    label: '按键',
    value: 'key'
  }
]
const buttons = [
  {
    color:"#afdfe4",
    context:"孩子不懂事Q着玩的",
    value: "alwaysQ"
  },
  {
    color:"#fe6673",
    context:"开发者自定义",
    value: "developer"
  },{
    color:"#ff0000",
    context:"终止线程",
    value: "shutdown"
  },
]

function run(value: any){
  console.log(value)
  if (value == 'shutdown'){
    shutdown()
  }
  if (value == 'alwaysQ'){
    for ( let i = 0 ; i <= 30; i++){
      keypress('Q')
      keypress('Q')
      keypress('Q')
      keypress('Q')
      keypress('Q')
      keypress('Q')
      keypress('Q')
      keypress('Q')
      keypress('Q')
      keypress('Q')
    }
  }
}

function checkFile(){
  sendData("test",{
    operate:selectValue.value,
    conf:mathValue.value
  })
}

function keypress(key){
  sendData("test",{
    operate:'press',
    key
  })
}

function autoClickFire(){
  window.api.system_notification("🔧🔧🔧🔧🔧", "现在开始自动点击心火")
  sendData("auto", {
    "operate":"click_fire"
  })
}

function shutdown(){
  window.api.system_notification("⛔⛔⛔⛔⛔", "终止！！！！！")
  sendData("auto", {
    "operate":"shutdown"
  })
}
</script>

<style scoped>
.father {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.dynamicButtonStyles{
    height: 50px;
    width: 50px;
    margin-left: 5px;
    font-size: 20px;
}
.dynamicSpaceStyles{
  margin-top: 10px;
}
</style>
