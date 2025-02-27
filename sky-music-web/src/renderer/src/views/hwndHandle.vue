<template>
  <div id="father">
    <n-gradient-text
      :gradient="{
        from: '	rgb(254, 1, 1)',
        to: 'rgb(254,115,1)',
      }"
      id="WindHide"
    >
    ! ! ! W A R N I N G ! ! !
  </n-gradient-text>
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      display: 'inline-block',
      color: 'black',
      background: '#f58f98',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText2" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      display: 'inline-block',
      color: 'black',
      background: '#f58f98',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <div style="flex-basis: 100%; margin-top: 8px;" />
    <n-button type="primary" color="#A3F6EC" ghost @click="getHwndMesseage()">
        刷新列表
    </n-button>
    <n-button type="primary" color="#f58f98" ghost @click="resetKeyToDefault()" style="margin-left: 10px;">
        重置为光遇窗口
    </n-button>
    <div style="flex-basis: 100%; margin-top: 8px;" />
    <n-gradient-text
        :gradient="{
          from: 'rgb(242,201,196)',
          to: 'rgb(221,242,196)',
        }"
        id="WindHide"
      >
      Now Hwnd > {{ nowHwnd == null ? 'nothing here' : nowHwnd }}
    </n-gradient-text>
    <n-data-table :columns="hwndColumns" :data="hwndColumnsList" :bordered="false" :min-row-height="48" ref="systemMusic"
          :max-height="430" :virtual-scroll="hwndColumnsList?.length > 7" row-class-name="td_css"
          style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
  </div>
</template>

<script setup lang="ts">
import { NButton, useThemeVars } from "naive-ui";
import { sendData } from "@renderer/utils/fetchUtils";
import { useMessage } from 'naive-ui'
import { h, onMounted, onUnmounted, ref } from 'vue'

const themeVars = useThemeVars();
const message = useMessage()
const headText = "此处为更改后台发送的目标，除了光遇以外的游戏均未测试，不会进行修复";
const headText2 = "因为此功能导致其他游戏被封号，不要找我。取决于游戏的反作弊机制";
const patterns = ["更改后台发送的目标", "光遇", "未测试", "不会", "不要找我", "导致", "封号", "反作弊机制"];
const hwndColumnsList = ref([])
const nowHwnd = ref("")
const hwndColumns = [
  {
    title: '软件标题',
    key: 'title',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },{
    title: '进程名字',
    key: 'exe_name',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },{
    title: 'PID',
    key: 'pid',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },{
    title: '句柄',
    key: 'hwnd',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '选定',
    key: 'operation',
    width: 60,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text: true,
          onClick: () => setHwndMesseage(row)
        },
        {
          default: () => {
            return '👈'
          }
        }
      )
    }
  }
]


function resetKeyToDefault(){
  setHwndMesseage('reset')
  message.success("重置")
}

function getHwndMesseage(){
  hwndColumnsList.value.length = 0
  sendData("config_operate",{
    "operate":"hwnd_get"
  }).then(res=>{
    hwndColumnsList.value = res
  })
}

function setHwndMesseage(data: any){
  sendData("config_operate",{
    "operate":"hwnd_set",
    "value": data
  })
}

function getNowHwndMesseage(){
  sendData("config_operate",{
    "operate":"hwnd_get_now",
    "value": "get"
  }).then(res=>{
    nowHwnd.value = res
  })
}
let nowHwndMesseageInterval:any = null
onMounted(() => {
  getHwndMesseage()
  nowHwndMesseageInterval = setInterval(getNowHwndMesseage,1000)
})

onUnmounted(() => {
  clearInterval(nowHwndMesseageInterval)
})
</script>

<style scoped>
@import url(https://fonts.googleapis.com/css?family=Shrikhand);

#WindHide {
  font-size: 30px;
  font-weight: bolder;
  font-family: "Shrikhand";
  margin-bottom: 9px;
}

#father {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

:deep(.td_css td) {
  color: #A3F6EC !important;
}
:deep(.th_css){
  color: #D0BDF4 !important;
}
</style>