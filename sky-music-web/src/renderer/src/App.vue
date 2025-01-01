<template>
  <n-config-provider :theme="darkTheme" :style="bronWidth === 800 ? '' : 'background-color: rgba(0, 0, 0, 0.5)'">
    <n-flex id="drag-area" justify="end" style="position: fixed; z-index: 200; right: 12px" :style="{
      width: collapsed ? '90%' : '80%'
    }">
      <n-button circle ghost dashed type="warning" style="margin-top: 12px" @click="openFileHandle" v-show="bronWidth === 800">
        📁
      </n-button>
      <n-button circle :dashed="fixDashed" ghost type="warning" style="margin-top: 12px" @click="fixHandle">
        📌
      </n-button>
      <n-button circle ghost type="info" style="margin-top: 12px" @click="miniHandle" v-show="bronWidth === 800">
        <template #icon>
          <n-icon>
            <Remove />
          </n-icon>
        </template>
      </n-button>
      <n-button circle ghost type="error" style="margin-top: 12px" @click="closeHandle">
        <template #icon>
          <n-icon>
            <Close />
          </n-icon>
        </template>
      </n-button>
    </n-flex>
    <n-spin :show="show" :size="90" :style="bronWidth === 800 ? 'background-color: black' : 'background-color: rgba(0, 0, 0, 0)'">
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
      <template #description> 🍉应用加载中，请稍等~ </template>
    </n-spin>
  </n-config-provider>
</template>

<script lang="ts" setup>
import type { Component } from 'vue'
import { h, onMounted, ref } from 'vue'
import { NIcon, darkTheme, NMessageProvider } from 'naive-ui'
import { getData } from '@renderer/utils/fetchUtils'
import {
  CubeSharp,
  Home,
  MusicalNotes,
  GameController,
  Library,
  Close,
  Remove,
} from '@vicons/ionicons5'
import router from '@renderer/router'

import { useRoute } from 'vue-router'
let bronWidth = window.innerWidth
const route = useRoute()
const collapsed = ref(false)
function fixHandle() {
  if (fixDashed.value) {
    window.api.setAlwaysOnTop();
    fixDashed.value = false
  } else {
    window.api.setAlwaysOnTop();
    fixDashed.value = true
  }
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
}
</style>
