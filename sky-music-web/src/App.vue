<template>
  <n-config-provider :theme="darkTheme">
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
              style="max-height: 739px; height: 739px"
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
  </n-config-provider>
</template>

<script lang="ts" setup>
import type { Component } from "vue";
import { defineComponent, h, ref } from "vue";
import { MenuOption, NIcon, darkTheme, NMessageProvider } from "naive-ui";
import { getData } from "@/utils/fetchUtils";
import {
  CubeSharp as CubeSharp,
  Home as Home,
  MusicalNotes as MusicalNotes,
  Cog as Cog,
} from "@vicons/ionicons5";
import router from "@/router";

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

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
    label: "音乐扒谱",
    key: "kube",
    icon: renderIcon(CubeSharp),
  }
];

const clickMenu = (key: string, item: MenuOption) => {
  router.push({ name: key });
};

let interval = setInterval(function () {
  windowsActive();
}, 1000);

function windowsActive() {
  getData("getWindowState").then((res) => {
    if (res) {
      document.title = "星星弹琴 - 游戏已运行 - haveFun!";
      clearInterval(interval);
    } else {
      document.title = "星星弹琴 - 当前未检测到游戏运行，请运行游戏！";
    }
  });
}
</script>
