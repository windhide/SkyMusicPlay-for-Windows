<template>
  <n-config-provider :theme="darkTheme" :style="{ opacity : transparency_number}" >
    <n-flex id="drag-area" justify="end" style="position: fixed; z-index: 200; right: 18px" :style="{ width: collapsed ? '90%' : '80%'}">
      <n-popselect v-model:value="nowLang" :options="options" trigger="click" @update:value="changeLang" scrollable>
          <n-button text size="large" color="#A3F6EC" style="margin-top: 12px; font-size: 20px;" :round="false"> 
            <n-icon size="25px">
              <Language />
            </n-icon> 
          </n-button>
      </n-popselect>
      <n-popover style="border-radius: 17px; --n-color: rgba(47,47,55,1)" trigger="click">
        <template #trigger>
          <n-button text size="large" color="#A3F6EC" style="margin-top: 12px; font-size: 20px;" :round="false"> 
            <n-icon size="25px">
              <ColorPaletteOutline />
            </n-icon> 
          </n-button>
        </template>
        <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">{{ t('main.transparency') }}</n-gradient-text>
        <n-slider v-model:value="transparency_number" :step="0.01" :max="1" :min="0" style="width: 200px;"/>
        <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">{{ t('main.color') }}</n-gradient-text>
        <n-color-picker :show-alpha="false" v-model:value="colorPick"/>
      </n-popover>
      <n-popover style="border-radius: 17px; --n-color: rgba(47,47,55,1)" trigger="click">
        <template #trigger>
          <n-button text size="large" color="#D0BDF4" style="margin-top: 12px; font-size: 20px;" :round="false"> 
            <n-icon size="25px">
              <Settings48Regular />
            </n-icon> 
          </n-button>
        </template>
        <n-switch size="small" v-model:value="is_compatibility_mode" @update:value="CompatibilityModeChange" :rail-style="railStyle" :round="false"> 
            <template #checked>
              <p style="color: rgba(94, 104, 81, 0.75);">{{ t('main.compatible') }}</p>
            </template>
            <template #unchecked>
              <p style="color: rgba(94, 104, 81, 0.75);">{{ t('main.backend') }}</p>
            </template>
          </n-switch> 
          <br>
          <n-switch size="small" v-model:value="isPostW" @update:value="PostWChange" :rail-style="railStyle" v-show="is_compatibility_mode != true" :round="false"> 
              <template #checked>
                <p style="color: rgba(94, 104, 81, 0.75);">{{ t('main.queue') }}</p>
              </template>
              <template #unchecked>
                <p style="color: rgba(94, 104, 81, 0.75);">{{ t('main.cut') }}</p>
              </template>
          </n-switch>
          <br>
          <n-switch size="small" v-model:value="isRunnable" @update:value="RunnableChange" :rail-style="railStyle" v-show="is_compatibility_mode != true" :round="false"> 
              <template #checked>
                <p style="color: rgba(94, 104, 81, 0.75);">{{ t('main.multi_core') }}</p>
              </template>
              <template #unchecked>
                <p style="color: rgba(94, 104, 81, 0.75);">{{ t('main.single_core') }}</p>
              </template>
          </n-switch>
      </n-popover>
      <n-button text :dashed="fixDashed" size="large" color="#F2C9C4" style="margin-top: 12px; font-size: 20px;" @click="fixHandle">
        <n-icon size="25px">
          <Pin48Regular v-if="fixDashed" />
          <Pin48Filled v-else />
        </n-icon>
      </n-button>
      <n-button text type="warning" size="large" style="margin-top: 12px; font-size: 20px;" @click="openFileHandle">
        <n-icon size="25px">
          <ImageOutline />
        </n-icon>
      </n-button>
      <n-button text type="info" size="large" style="margin-top: 12px; font-size: 25px;" @click="miniHandle">
          <n-icon>
            <RemoveSharp />
          </n-icon>
      </n-button>
      <n-button text type="error" size="large" style="margin-top: 12px; font-size: 25px;" @click="closeHandle">
          <n-icon>
            <Close />
          </n-icon>
      </n-button>
    </n-flex>
    <n-spin :show="show" :size="90" stroke="#F2E8C4">
      <n-message-provider>
        <n-dialog-provider>
          <n-space vertical>
            <n-layout>
              <n-layout has-sider>
                <n-layout-sider  v-show="route.fullPath.indexOf('keyboard') == -1" bordered show-trigger 
                  collapse-mode="width" :collapsed-width="64" :width="150" :native-scrollbar="false" @update:collapsed="collapsedHandle"
                  :style="{
                    height: '100vh',
                    backgroundColor: colorPick+ ' !important'
                  }"
                  >
                  <n-menu :collapsed-width="64" :collapsed-icon-size="23" :options="menuOptions"
                    @update:value="clickMenu" />
                </n-layout-sider>
                  <n-layout 
                  :style="{
                    padding: '30px 20px 0px 20px',
                    backgroundColor: colorPick+' !important'
                  }"
                  >
                  <router-view />
                </n-layout>
              </n-layout>
            </n-layout>
          </n-space>
        </n-dialog-provider>
      </n-message-provider>
      <template #description> <div style="color: #F2E8C4;">{{ t('main.loading') }}</div> </template>
    </n-spin>
  </n-config-provider>
</template>

<script lang="ts" setup>
import type { Component, CSSProperties } from 'vue'
import { h, onMounted, ref, nextTick, computed } from 'vue'
import { NIcon, darkTheme, NMessageProvider } from 'naive-ui'
import { getData, sendData } from '@renderer/utils/fetchUtils'
import {
  CubeSharp,
  Home,
  MusicalNotes,
  GameController,
  Close,
  RemoveSharp,
  Flask,
  ImageOutline,
  Settings,
  PlanetSharp,
  ColorPaletteOutline,
  PulseSharp,
  Language
} from '@vicons/ionicons5'
import {
  Pin48Regular,
  Pin48Filled,
  Settings48Regular,
  Compose24Filled
} from '@vicons/fluent'
import router from '@renderer/router'

import { useRoute } from 'vue-router'
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n();
const route = useRoute()
const collapsed = ref(false)
const is_compatibility_mode = ref(false)
const isPostW = ref(true)
const isRunnable = ref(true)
const transparency_number = ref(1.00)
const colorPick = ref("#101014")
const nowLang = ref('zh_cn')
const options = [
  {
    label: "简体中文",
    value: "zh_cn"
  },
  {
    label: "文言文",
    value: "zh_classical"
  },
  {
    label: "繁體中文",
    value: "zh_tw"
  },
  {
    label: "English",
    value: "en"
  },
  {
    label: "日本語",
    value: "jp"
  },
  {
    label: "한국어",
    value: "ko"
  }
];

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
  sendData('openFiles',{
      "operate":"images"
  })
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
const menuOptions = computed(() => [
  {
    label: t('main.menu.home'),
    key: "home",
    icon: renderIcon(Home),
  },
  {
    label: t('main.menu.music'),
    key: "music",
    icon: renderIcon(MusicalNotes),
  },
  {
    label: t('main.menu.tutorial'),
    key: "tutorial",
    icon: renderIcon(GameController),
  },
  {
    label: t('main.menu.kube'),
    key: "kube",
    icon: renderIcon(CubeSharp),
  },
  {
    label: t('main.menu.shortcut'),
    key: "shortcut",
    icon: renderIcon(PlanetSharp),
  },
  {
    label: t('main.menu.musicEdit'),
    key: "musicEdit",
    icon: renderIcon(Compose24Filled),
  },
  {
    key: "kube",
    type: "divider"
  },
  {
    label: t('main.menu.setting'),
    key: "setting",
    icon: renderIcon(Settings),
  },
  {
    label: t('main.menu.hwndHandle'),
    key: "hwndHandle",
    icon: renderIcon(PulseSharp),
  },
  {
    label: t('main.menu.magicTools'),
    key: "magicTools",
    icon: renderIcon(Flask),
  },
]);

const clickMenu = (key: string) => {
  router.push({ name: key });
};

let checkInterval = setInterval(() => {
  getData("check").then(res => {
    if (res === undefined) return
    show.value = !res
    clearInterval(checkInterval)
    LoadData()
    window.api.sync_el_2_sheet()
    router.push({ name: 'home', query: { show: 1 } });
  });
}, 500)

function CompatibilityModeChange(value: boolean){
  sendData("config_operate",{
    operate:"set",
    name:"compatibility_mode",
    value
  })
}

function PostWChange(value: boolean){
  sendData("config_operate",{
    operate:"set",
    name:"is_post_w",
    value
  })
}

function RunnableChange(value: boolean){
  sendData("config_operate",{
    operate: "set",
    name: "cpu_type",
    value
  })
}

function changeLang(value: string) {
  // 更新locale值并保存到localStorage
  locale.value = value
  localStorage.setItem('sky-music-language', value)
  show.value = true
  nextTick(async () => {
    const newMenuOptions = [
      {
        label: t('main.menu.home'),
        key: "home",
        icon: renderIcon(Home),
      },
      {
        label: t('main.menu.music'),
        key: "music",
        icon: renderIcon(MusicalNotes),
      },
      {
        label: t('main.menu.tutorial'),
        key: "tutorial",
        icon: renderIcon(GameController),
      },
      {
        label: t('main.menu.kube'),
        key: "kube",
        icon: renderIcon(CubeSharp),
      },
      {
        label: t('main.menu.shortcut'),
        key: "shortcut",
        icon: renderIcon(PlanetSharp),
      },
      {
        label: t('main.menu.musicEdit'),
        key: "musicEdit",
        icon: renderIcon(Compose24Filled),
      },
      {
        key: "kube",
        type: "divider"
      },
      {
        label: t('main.menu.setting'),
        key: "setting",
        icon: renderIcon(Settings),
      },
      {
        label: t('main.menu.hwndHandle'),
        key: "hwndHandle",
        icon: renderIcon(PulseSharp),
      },
      {
        label: t('main.menu.magicTools'),
        key: "magicTools",
        icon: renderIcon(Flask),
      }
    ]
    Object.assign(menuOptions, newMenuOptions)
    const currentRoute = route.name
    // 跳转到设置页再跳回原页面，切换过程中显示Loading
    let target = currentRoute
    await router.push({ name: 'setting' })
    await nextTick()
    await router.push({ name: target })
    show.value = false
  })
}

function LoadData(){
  sendData("config_operate",{
    operate: "cpu_type" 
  }).then(res=>{
    isRunnable.value = res
  })
}

onMounted(() => {
  // 从localStorage获取保存的语言设置，初始化当前语言
  const savedLanguage = localStorage.getItem('sky-music-language')
  if (savedLanguage) {
    nowLang.value = savedLanguage
    locale.value = savedLanguage
  }

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
  --n-item-icon-color-collapsed: rgba(221,242,196, 0.82) !important;
}
:deep(.n-menu-item-content){
  --n-item-text-color: rgba(221,242,196, 0.82) !important;
  --n-item-text-color-hover: rgb(242,201,196) !important;
  color: rgba(94, 104, 81, 0.82);
}
:deep(.n-slider-rail__fill){
  --n-fill-color-hover: #A3F6EC !important;
  background-color: #A3F6EC !important;
}
</style>

<style>
.n-card {
  background-color: rgba(242, 201, 196, 0) !important;
}
.n-menu-divider {
  margin-bottom: 325px;
  background-color: rgba(242, 201, 196, 0);
}
.n-drawer-mask,.n-drawer{
  border-radius: 26px !important;
}
</style>