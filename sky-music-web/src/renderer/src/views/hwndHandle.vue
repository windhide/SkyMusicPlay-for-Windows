<template>
  <div id="father">
    <n-gradient-text
      :gradient="{
        from: '	rgb(254, 1, 1)',
        to: 'rgb(254,115,1)',
      }"
      id="WindHide"
    >
    W A R N I N G
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
        {{t("hwnd_handle.refresh")}}
    </n-button>
    <n-button type="primary" color="#f58f98" ghost @click="resetKeyToDefault()" style="margin-left: 10px;">
        {{t("hwnd_handle.reset_sky")}}
    </n-button>
    <div style="flex-basis: 100%; margin-top: 8px;" />
    <n-gradient-text
        :gradient="{
          from: 'rgb(242,201,196)',
          to: 'rgb(221,242,196)',
        }"
        id="hwnd"
      >
      {{t("hwnd_handle.now_hwnd")}} {{ nowHwnd == null ? 'Nothing' : nowHwnd }}
    </n-gradient-text>
    <n-data-table :columns="hwndColumns" :data="hwndColumnsList" :bordered="false" :min-row-height="48" ref="systemMusic"
          :max-height="475" :virtual-scroll="hwndColumnsList?.length > 7" row-class-name="td_css"
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
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const themeVars = useThemeVars();
const message = useMessage()
const headText = t("hwnd_handle.head_text");
const headText2 = t("hwnd_handle.head_text2");
const patterns = [t("hwnd_handle.patterns0"),t("hwnd_handle.patterns1"),t("hwnd_handle.patterns2"),t("hwnd_handle.patterns3"),t("hwnd_handle.patterns4"),t("hwnd_handle.patterns5"),t("hwnd_handle.patterns6"),t("hwnd_handle.patterns7")];
const hwndColumnsList = ref([])
const nowHwnd = ref("")
const hwndColumns = [
  {
    title: t("hwnd_handle.columns.title"),
    key: 'title',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },{
    title: t("hwnd_handle.columns.exe_name"),
    key: 'exe_name',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },{
    title: t("hwnd_handle.columns.pid"),
    key: 'pid',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },{
    title: t("hwnd_handle.columns.hwnd"),
    key: 'hwnd',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: t("hwnd_handle.columns.operation"),
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
  message.success(t("hwnd_handle.reset"))
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

#hwnd {
  font-size: 20px;
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