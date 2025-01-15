<template>
  <div class="father">
    <n-divider>
      <n-button text style="font-size: 30px" @click="layoutChange('isScriptShow')">
        ⚠
      </n-button>
      <n-button text style="font-size: 30px" @click="layoutChange('isTestShow')">
        🚧
      </n-button>
    </n-divider>
    <div class="father" v-show="isScriptShow">
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
      <div style="flex: 0 0 100%;" class="father">
        <n-button type="warning" ghost @click="autoClickFire">
          自动点火（站在星盘上，确保游戏出现了G，再点本按钮）
        </n-button>
      </div>
      <n-divider />
      <div class="father" v-for="button in buttons">
        <n-button dashed :color=button.color @click="run(button.value)"
          :style="{ marginTop: '30px', marginLeft: button.value === 'all' ? '0' : '15px' }"
          v-if="button.value != 'developer'">
          {{ button.context }}
        </n-button>
        <n-upload v-else action="http://localhost:9899/autoScriptUpload" style="margin-top:30px" accept=".txt"
          :show-file-list="false">
          <n-button type="info" dashed :color=button.color> {{ button.context }}</n-button>
        </n-upload>
      </div>
      <n-space vertical style="flex: 0 0 100%; margin-top:30px" class="father">
        <n-el>
          <n-progress type="multiple-circle" :stroke-width="6" :circle-gap="0.3" :percentage="percentage"
            :color="ringColor.activate" :rail-style="ringColor.not_activate">
            <div style="text-align: center">
              进度
            </div>
          </n-progress>
        </n-el>
      </n-space>
    </div>
    <div class="father" v-show="isTestShow">
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
      <div class="father" v-for="button in devButtons">
        <n-button dashed :color=button.color @click="run(button.value)"
          :style="{marginLeft: button.value === 'all' ? '0' : '15px' }"
          v-if="button.value != 'developer'">
          {{ button.context }}
        </n-button>
        <n-upload v-else action="http://localhost:9899/autoScriptUpload" accept=".txt"
          :show-file-list="false">
          <n-button type="info" dashed :color=button.color> {{ button.context }}</n-button>
        </n-upload>
      </div>
      <n-divider />
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
const isScriptShow = ref(false)
const isTestShow = ref(false)
const themeVars = useThemeVars();
const headText = "此处是测试版功能请谨慎使用🌶，不涉及内存修改🌶。";
const headText2 = "此处功能仅供学习交流，严禁用于商业用途，请于24小时内删除";
const headText3 = "🚫模拟器玩家禁止使用下面的所有功能🚫";
const patterns = ["谨慎使用🌶", "不涉及内存修改🌶", "此处功能仅供学习交流，严禁用于商业用途，请于24小时内删除", "🚫模拟器玩家禁止使用下面的所有功能🚫"];
const percentage = [0,0,0,0,0]
const ringColor = {
  activate:['#cde6c7','#afdfe4','#f3704b','#45b97c','#33a3dc'],
  not_activate:[{ stroke: '#cde6c7', opacity: 0.2 },{ stroke: '#afdfe4', opacity: 0.2 },{ stroke: '#f3704b', opacity: 0.2 },{ stroke: '#45b97c', opacity: 0.2 },{ stroke: '#33a3dc', opacity: 0.2 }]
}
let mathValue = ref(0)
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
    color:"#f0dc70",
    context:"全图",
    value: "all"
  },{
    color:"#cde6c7",
    context:"云野",
    value: "prairie"
  },{
    color:"#afdfe4",
    context:"雨林",
    value: "forest"
  },{
    color:"#f3704b",
    context:"霞谷",
    value: "valley"
  },{
    color:"#45b97c",
    context:"墓土",
    value: "wasteland"
  },{
    color:"#33a3dc",
    context:"禁阁",
    value: "library"
  },{
    color:"#2ae0c8",
    context:"挂机",
    value: "afk"
  },{
    color:"#ff0000",
    context:"终止线程",
    value: "shutdown"
  }
]

const devButtons = [{
    color:"#fe6673",
    context:"开发者自定义",
    value: "developer"
  },{
    color:"#ff0000",
    context:"终止线程",
    value: "shutdown"
  }
]


function run(value: any){
  console.log(value)
  if (value == 'shutdown'){
    shutdown()
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

function layoutChange(layout){
  eval(layout + '.value = !' + layout + '.value')
  switch(layout){
    case 'isTestShow':
      isScriptShow.value = !isTestShow.value
      break
    case 'isScriptShow':
      isTestShow.value = !isScriptShow.value
      break
  }
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
  margin-top: 5px;
}
</style>
