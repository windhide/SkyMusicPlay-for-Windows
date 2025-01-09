<template>
  <n-config-provider :theme="darkTheme" :style="bronWidth === 800 ? '' : 'background-color: rgba(0, 0, 0, 0.5)'">
    <n-flex id="drag-area" justify="end" style="position: fixed; z-index: 200; right: 18px" :style="{
      width: collapsed ? '90%' : '80%'
    }">
      <n-popover style="border-radius: 25px;" trigger="click">
        <template #trigger>
          <n-button text size="large" type="warning" style="margin-top: 12px; font-size: 20px;" :round="false"> 
            <n-icon size="25px">
              <Settings48Regular />
            </n-icon> 
          </n-button>
        </template>
        <n-switch size="small" v-model:value="isSimulator" @update:value="SimulatorChange" :rail-style="railStyle"> 
            <template #checked>
              <p style="color: rgba(94, 104, 81, 0.65);">兼容模式</p>
            </template>
            <template #unchecked>
              <p style="color: rgba(94, 104, 81, 0.65);">后台模式</p>
            </template>
          </n-switch> 
      </n-popover>
      <n-button text :dashed="fixDashed" size="large" type="warning" style="margin-top: 12px; font-size: 20px; margin-right: 3px;" @click="fixHandle">
        <n-icon size="25px">
          <Pin48Regular v-if="fixDashed" />
          <Pin48Filled v-else />
        </n-icon>
      </n-button>
      <n-button text type="warning" size="large" style="margin-top: 12px; font-size: 20px;" @click="openFileHandle" v-show="bronWidth === 800">
        <n-icon size="25px">
          <ImageOutline />
        </n-icon>
      </n-button>
      <n-button text type="info" size="large" style="margin-top: 12px; font-size: 25px;" @click="miniHandle" v-show="bronWidth === 800">
          <n-icon>
            <Remove />
          </n-icon>
      </n-button>
      <n-button text type="error" size="large" style="margin-top: 12px; font-size: 25px;" @click="closeHandle">
          <n-icon>
            <Close />
          </n-icon>
      </n-button>
    </n-flex>
    <n-spin :show="show" :size="90" :style="bronWidth === 800 ? 'background-color: black;' : 'background-color: rgba(0, 0, 0, 0)'" stroke="#F2E8C4">
      <n-message-provider>
        <n-dialog-provider>
          <n-space vertical>
            <n-layout :style="bronWidth === 800 ? '' : 'background-color: rgba(0, 0, 0, 0)'">
              <n-layout has-sider :style="bronWidth === 800 ? '' : 'background-color: rgba(0, 0, 0, 0)'">
                <n-layout-sider v-show="route.fullPath.indexOf('keyboard') == -1" bordered show-trigger
                  collapse-mode="width" :collapsed-width="64" :width="150" :native-scrollbar="false"
                  style="height: 100vh" @update:collapsed="collapsedHandle">
                  <n-menu :collapsed-width="64" :collapsed-icon-size="22" :options="menuOptions"
                    @update:value="clickMenu" />
                </n-layout-sider>
                <n-layout :style="bronWidth === 800 ? 'padding: 40px 25px 0px 25px' : 'background-color: rgba(0, 0, 0, 0)'">
                  <router-view />
                </n-layout>
              </n-layout>
            </n-layout>
          </n-space>
        </n-dialog-provider>
      </n-message-provider>
      <template #description> <div style="color: #F2E8C4;">🍉应用加载中，请稍等~</div> </template>
    </n-spin>
  </n-config-provider>
</template>

<script lang="ts" setup>
import type { Component, CSSProperties } from 'vue'
import { h, onMounted, ref } from 'vue'
import { NIcon, darkTheme, NMessageProvider } from 'naive-ui'
import { getData, sendData } from '@renderer/utils/fetchUtils'
import {
  CubeSharp,
  Home,
  MusicalNotes,
  GameController,
  Library,
  Close,
  Remove,
  Flask,
  ImageOutline
} from '@vicons/ionicons5'
import {
  Pin48Regular,
  Pin48Filled,
  Settings48Regular
} from '@vicons/fluent'
import router from '@renderer/router'

import { useRoute } from 'vue-router'
let bronWidth = window.innerWidth
const route = useRoute()
const collapsed = ref(false)
const isSimulator = ref(false)
function fixHandle() {
  if (fixDashed.value) {
    window.api.setAlwaysOnTop();
    fixDashed.value = false
  } else {
    window.api.setAlwaysOnTop();
    fixDashed.value = true
  }
}

function railStyle({ focused, checked }){
        const style: CSSProperties = {}
        if (checked) {
          style.background = '#F2C9C4'
          if (focused) {
            style.boxShadow = '0 0 0 2px #F2C9C440'
          }
        }
        else {
          style.background = '#F2E8C4'
          if (focused) {
            style.boxShadow = '0 0 0 2px #F2E8C440'
          }
        }
        return style
}

function openFileHandle() {
  getData('openFiles')
}

function miniHandle() {
  window.api.mini()
}
function closeHandle() {
  window.api.close()
}

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

const collapsedHandle = (isCoolapsed: boolean) => {
  console.log(isCoolapsed)
  collapsed.value = isCoolapsed
}

let show = ref(true)
let fixDashed = ref(true)
const menuOptions = [
  {
    label: "介绍",
    key: "home",
    icon: renderIcon(Home),
  },
  {
    label: "音乐",
    key: "music",
    icon: renderIcon(MusicalNotes),
  },
  {
    label: "跟弹",
    key: "tutorial",
    icon: renderIcon(GameController),
  },
  {
    label: "音乐扒谱",
    key: "kube",
    icon: renderIcon(CubeSharp),
  },
  {
    label: "生成乐谱",
    key: "sheetPdf",
    icon: renderIcon(Library),
  },
  {
    label: "开发者功能",
    key: "magicTools",
    icon: renderIcon(Flask),
  }
];

const clickMenu = (key: string) => {
  router.push({ name: key });
};

router.push({ name: 'home' });

let checkInterval = setInterval(() => {
  getData("check").then(res => {
    if (res === undefined) return
    show.value = !res
    clearInterval(checkInterval)
  });
}, 500)

function SimulatorChange(value: boolean){
  sendData("config_operate",{
    operate:"set",
    name:"is_simulator",
    value
  })
}

onMounted(() => {
  const dragArea = document.getElementById('drag-area')
  if (dragArea) {
    let startX, startY

    dragArea.addEventListener('mousedown', (event) => {
      startX = event.clientX
      startY = event.clientY

      window.electron.onMouseDown(startX, startY)
      const onMouseMove = (moveEvent) => {
        const deltaX = moveEvent.clientX - startX
        const deltaY = moveEvent.clientY - startY
        window.electron.onMouseMove(deltaX, deltaY)
      }
      const onMouseUp = () => {
        document.removeEventListener('mousemove', onMouseMove)
        document.removeEventListener('mouseup', onMouseUp)
        window.electron.onMouseUp()
      }

      document.addEventListener('mousemove', onMouseMove)
      document.addEventListener('mouseup', onMouseUp)
    })
  } else {
    console.error('drag-area element not found')
  }
})
</script>

<style scoped>
:deep(.n-menu--vertical){
  --n-border-radius: 21px !important;
  --n-item-text-color-active: rgb(242,232,196) !important;
  --n-item-icon-color-active: rgb(242,232,196) !important;
  --n-item-text-color-active-hover: rgb(242,232,196) !important;
  --n-item-icon-color: rgba(221,242,196, 0.82) !important;
  --n-item-icon-color-hover:  rgb(242,201,196) !important;
  --n-item-icon-color-active: rgb(242,232,196) !important;
  --n-item-icon-color-active-hover: rgb(242,232,196) !important;
  --n-item-icon-color-child-active: rgb(242,232,196) !important;
  --n-item-icon-color-child-active-hover: rgb(242,232,196) !important;
  --n-item-icon-color-collapsed: rgba(255, 255, 255, 0.9);
  --n-item-color-active: rgba(242,232,196,0.15) !important;
  --n-item-color-active-hover: rgba(242,232,196,0.3) !important;
}
:deep(.n-menu-item-content){
  --n-item-text-color: rgba(221,242,196, 0.82) !important;
  --n-item-text-color-hover: rgb(242,201,196) !important;
  color: rgba(94, 104, 81, 0.82);
}
</style>
