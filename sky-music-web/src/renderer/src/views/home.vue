<template>
  <div id="father">
    <n-divider>
      <img
        id="avatar"
        src="https://s1.imagehub.cc/images/2025/01/13/47f2e793dc71cd0719575340939d814b.png"
      />
    </n-divider>
    <n-highlight
      style="margin-bottom: 5px; color: #DDF2C4;"
      :text="headText"
      :patterns="patterns"
      :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2C9C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }"
    />
    <n-highlight
      style="color: #DDF2C4;"
      :text="text"
      :patterns="patterns"
      :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2C9C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }"
    />
    <n-divider>
      <n-gradient-text type="info" :size="25" style="color:#F2C9C4"> 
        <n-button ghost color="#F2C9C4"  @click="blankClick('https://windhide.netlify.app')"  style="font-size: 20px">
          查看教使用教程
        </n-button> 
      </n-gradient-text>
    </n-divider>
    <n-button type="info" color="#F2C9C4" text  @click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows/pulls')"  style="font-size: 30px">
      <n-icon>
        <GitPullRequest />
      </n-icon>
    </n-button>
    <n-button type="info" color="#F2E8C4" text  @click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows')" style="margin-left: 20px; font-size: 30px">
      <n-icon>
        <LogoGithub />
      </n-icon>
    </n-button>
    <n-button type="info" color="#DDF2C4" text  @click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows/issues/new')" style="margin-left: 20px; font-size: 30px">
      <n-icon>
        <Build />
      </n-icon>
    </n-button>
  </div>
</template>

<script setup lang="ts">
import { useThemeVars } from "naive-ui";
import { GitPullRequest, LogoGithub, Build } from "@vicons/ionicons5";
import { sendData, getData, getWWWData } from "@renderer/utils/fetchUtils";
import router from "@renderer/router";
import { useDialog } from "naive-ui";

const themeVars = useThemeVars();
const headText = "如果您觉得好用可以赏我一杯咖啡☕";
const text = "欢迎使用本软件，本软件完全免费，如果您是买的本软件就是被骗了";
const patterns = ["完全免费", "被骗了", "咖啡☕"];
const dialog = useDialog();

function blankClick(url) {
  getData("openBrowser?url=" + url);
}

function jump() {
  if (window.innerWidth == 800) {
    return;
  }
  sendData("follow", { type: "不ok", operate: 'nextSheet' }).then((res) => {
    if (res.length != 0) router.push({ name: "keyboard" });
  });
}

let updateInterval = setInterval(()=>{
  if (window.innerWidth == 800) {
    window.api.getVersion().then((cilentVersion) => {
      getData("update").then((cloudVersion: any) => {
        if (cloudVersion == null) clearInterval(updateInterval)
        if (
          cloudVersion.version.match(/\d/g).join("") > cilentVersion.match(/\d/g).join("")
        ) {
          dialog.success({
            title: cloudVersion.title,
            content: cloudVersion.content?.replaceAll("\\n","\n").replaceAll("\\t","\t"),
            positiveText: cloudVersion.positiveText,
            negativeText: cloudVersion.negativeText,
            contentStyle: { whiteSpace: "pre-wrap" },
            onPositiveClick: () => {
              getData("openBrowser?url=" + cloudVersion.downloadUrl);
              clearInterval(updateInterval)
            },
            onNegativeClick: () => {
              clearInterval(updateInterval)
            }
          });
        }
      });
    });
  }
},2000)


jump();
</script>

<style scoped>
#father {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

#avatar {
  height: 250px;
  width: 250px;
}
</style>
