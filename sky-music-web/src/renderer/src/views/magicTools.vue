<template>
  <div class="father">
    <n-divider>
      <n-gradient-text type="error" :size="25"> 注意 </n-gradient-text>
    </n-divider>
    <n-highlight
      style="margin-bottom: 5px"
      :text="headText"
      :patterns="patterns"
      :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2E8C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }"
    />
    <n-divider />
    <div style="flex: 0 0 100%;" class="father">
      <n-button type="warning" ghost @click="autoClickFire">
        自动点火（使用前请把火和爱心都收了，不然会点不到）
      </n-button>
    </div>
    <div class="father" v-for="button in buttons">
      <n-button dashed :color=button.color @click="run(button.value)"  :style="{ marginTop: '30px', marginLeft: button.value === 'all' ? '0' : '15px' }" v-if="button.value != 'developer'" >
        {{ button.context }}
      </n-button>
      <n-upload v-else
        action="http://localhost:9899/autoScriptUpload"
        style="margin-top:30px"
        accept=".txt"
        :show-file-list="false"
      >
      <n-button type="info" dashed :color=button.color> {{ button.context }}</n-button>
      </n-upload>
    </div>
    <n-space vertical style="flex: 0 0 100%; margin-top:30px" class="father">
      <n-el>
        <n-progress
          type="multiple-circle"
          :stroke-width="6"
          :circle-gap="0.3"
          :percentage="percentage"
          :color="ringColor.activate"
          :rail-style="ringColor.not_activate"
        >
          <div style="text-align: center">
            进度
          </div>
        </n-progress>
    </n-el>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { getData } from "@renderer/utils/fetchUtils";
import { useThemeVars } from "naive-ui";
const themeVars = useThemeVars();
const headText = "此处是测试版功能请谨慎使用🌶，不涉及内存修改🌶";
const patterns = ["谨慎使用🌶", "不涉及内存修改🌶"];
const percentage = [0,0,0,0,0]
const ringColor = {
  activate:['#cde6c7','#afdfe4','#f3704b','#45b97c','#33a3dc'],
  not_activate:[{ stroke: '#cde6c7', opacity: 0.2 },{ stroke: '#afdfe4', opacity: 0.2 },{ stroke: '#f3704b', opacity: 0.2 },{ stroke: '#45b97c', opacity: 0.2 },{ stroke: '#33a3dc', opacity: 0.2 }]
}

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
    context:"挂机点我",
    value: "afk"
  },{
    color:"#fe6673",
    context:"开发者自定义",
    value: "developer"
  }
]

function run(value: any){
  console.log(value)
}


function autoClickFire(){
  window.api.system_notification("🔧🔧🔧🔧🔧", "现在开始自动点击心火")
  getData("autoClickFire").then(res=>{
    window.api.system_notification("❤❤❤❤❤", res)
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
</style>
