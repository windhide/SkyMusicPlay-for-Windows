<template>
  <n-config-provider :theme="darkTheme">
	  <n-spin :show="show" :size="90" style="background-color: black;">
    <n-message-provider>
      <n-space vertical>
        <n-layout>
          <n-layout has-sider>
            <n-layout-sider
              bordered
              show-trigger
              collapse-mode="width"
              :collapsed-width="64"
              :width="150"
              :native-scrollbar="false"
              style="max-height: 739px; height: 740px"
              v-show="$route.fullPath.indexOf('keyboard') == -1"
            >
              <n-menu
                :collapsed-width="64"
                :collapsed-icon-size="22"
                :options="menuOptions"
                @update:value="clickMenu"
              />
            </n-layout-sider>
            <n-layout style="max-height: 739px; padding: 25px">
              <router-view />
            </n-layout>
          </n-layout>
        </n-layout>
      </n-space>
    </n-message-provider>
      <template #description>
        🍉应用加载中，请稍等~
      </template>
    </n-spin>
  </n-config-provider>
</template>

<script lang="ts" setup>
import type { Component } from "vue";
import { h, ref } from "vue";
import { MenuOption, NIcon, darkTheme, NMessageProvider } from "naive-ui";
import { getData } from '@/utils/fetchUtils'
import {
  CubeSharp,
  Home,
  MusicalNotes,
  GameController
} from "@vicons/ionicons5";
import router from "@/router";

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

let show = ref(true)

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
];

const clickMenu = (key: string, item: MenuOption) => {
  router.push({ name: key });
};

router.push({ name: 'home' });

let checkInterval = setInterval(()=>{
  getData("check").then(res => {
    if(res === undefined) return
    show.value = !res
    clearInterval(checkInterval)
  });
},500)
</script>
