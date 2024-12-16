<template>
  <n-config-provider :theme="darkTheme">
    <n-flex justify="end" id="drag-area" style="position:fixed; top: 0;left: 0; z-index: 200;width: 99%;">
      <n-button circle :dashed="fixDashed" ghost type="warning" @click="fixHandle" style="margin-top: 12px;">
          📌
      </n-button>
      <n-button circle ghost type="info" @click="miniHandle" style="margin-top: 12px;">
        <template #icon>
          <n-icon><Remove /></n-icon>
        </template>
      </n-button>
      <n-button circle ghost type="error" @click="closeHandle" style="margin-top: 12px; margin-right: 5px;">
        <template #icon>
          <n-icon><Close /></n-icon>
        </template>
      </n-button>
    </n-flex>
    <n-spin :show="show" :size="90" style="background-color: black;">
      <n-message-provider>
        <n-dialog-provider>
          <n-space vertical>
            <n-layout>
              <n-layout has-sider>
                <n-layout-sider bordered show-trigger collapse-mode="width" :collapsed-width="64" :width="150"
                  :native-scrollbar="false" style="height: 100vh" v-show="$route.fullPath.indexOf('keyboard') == -1">
                  <n-menu :collapsed-width="64" :collapsed-icon-size="22" :options="menuOptions"
                    @update:value="clickMenu" />
                </n-layout-sider>
                <n-layout style="max-height: 739px; padding: 25px">
                  <router-view />
                </n-layout>
              </n-layout>
            </n-layout>
          </n-space>
        </n-dialog-provider>
      </n-message-provider>
      <template #description>
        🍉应用加载中，请稍等~
      </template>
    </n-spin>
  </n-config-provider>
</template>

<script lang="ts" setup>
import type { Component } from "vue";
import { h, onMounted, ref } from "vue";
import { MenuOption, NIcon, darkTheme, NMessageProvider } from "naive-ui";
import { getData } from '@/utils/fetchUtils'
import {
  CubeSharp,
  Home,
  MusicalNotes,
  GameController,
  Library,
  Close,
  Remove
} from "@vicons/ionicons5";
import router from "@/router";

function fixHandle() {
  if(fixDashed.value){
    window.api.setAlwaysOnTop(fixDashed.value); 
    fixDashed.value = false
  }else{
    window.api.setAlwaysOnTop(fixDashed.value); 
    fixDashed.value = true
  }
}

function miniHandle(){
  window.api.mini()
}
function closeHandle(){
  window.api.close()
}

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) });
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
];

const clickMenu = (key: string, item: MenuOption) => {
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
