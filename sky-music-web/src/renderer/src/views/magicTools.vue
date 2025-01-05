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
        background: 'cyan',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }"
    />
    <n-divider />
    <div style="flex: 0 0 100%;" class="father">
      <n-button type="warning" ghost @click="autoClickFire">
        自动点火（使用前请把火和爱心都收了，不然会点不到）
      </n-button>
    </div>
    <div style="flex: 0 0 100%; margin-top: 20px;" class="father">
      <n-button type="warning" dashed>
        自动跑图（开发中⚙）
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getData } from "@renderer/utils/fetchUtils";
import { useThemeVars } from "naive-ui";
const themeVars = useThemeVars();
const headText = "此处是测试版功能请谨慎使用⚙，不涉及内存修改🔧";
const patterns = ["谨慎使用⚙", "不涉及内存修改🔧", "咖啡☕"];

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
