<template>
  <div id="father">
    <n-space>
      <n-button class="buttonStyle" :color="isActive_Y" :type="isGhost_Y ? '' : 'primary'" :ghost="isGhost_Y">Y</n-button>
      <n-button class="buttonStyle" :color="isActive_U" :type="isGhost_U ? '' : 'primary'" :ghost="isGhost_U">U</n-button>
      <n-button class="buttonStyle" :color="isActive_I" :type="isGhost_I ? '' : 'primary'" :ghost="isGhost_I">I</n-button>
      <n-button class="buttonStyle" :color="isActive_O" :type="isGhost_O ? '' : 'primary'" :ghost="isGhost_O">O</n-button>
      <n-button class="buttonStyle" :color="isActive_P" :type="isGhost_P ? '' : 'primary'" :ghost="isGhost_P">P</n-button>
    </n-space>
    <n-space style="margin-top: 10px;">
      <n-button class="buttonStyle" :color="isActive_H" :type="isGhost_H ? '' : 'primary'" :ghost="isGhost_H">H</n-button>
      <n-button class="buttonStyle" :color="isActive_J" :type="isGhost_J ? '' : 'primary'" :ghost="isGhost_J">J</n-button>
      <n-button class="buttonStyle" :color="isActive_K" :type="isGhost_K ? '' : 'primary'" :ghost="isGhost_K">K</n-button>
      <n-button class="buttonStyle" :color="isActive_L" :type="isGhost_L ? '' : 'primary'" :ghost="isGhost_L">L</n-button>
      <n-button class="buttonStyle" :color="isActive_LL" :type="isGhost_LL ? '' : 'primary'" :ghost="isGhost_LL">;</n-button>
    </n-space>
    <n-space style="margin-top: 10px;">
      <n-button class="buttonStyle" :color="isActive_N" :type="isGhost_N ? '' : 'primary'" :ghost="isGhost_N">N</n-button>
      <n-button class="buttonStyle" :color="isActive_M" :type="isGhost_M ? '' : 'primary'" :ghost="isGhost_M">M</n-button>
      <n-button class="buttonStyle" :color="isActive_BB" :type="isGhost_BB ? '' : 'primary'" :ghost="isGhost_BB">,</n-button>
      <n-button class="buttonStyle" :color="isActive_NN" :type="isGhost_NN ? '' : 'primary'" :ghost="isGhost_NN">.</n-button>
      <n-button class="buttonStyle" :color="isActive_MM" :type="isGhost_MM ? '' : 'primary'" :ghost="isGhost_MM">/</n-button>
    </n-space>
  </div>
</template>

<style scoped>
#father {
  /* 带menu 289 不带315 */
  /* height: 289px; */
  height: 100vh;
  display: flex;
  justify-content: center;
  align-content: center;
  flex-wrap: wrap;
}

.buttonStyle {
  height: 60px;
  width: 60px;
}
</style>

<script setup lang="ts">
import { ref } from 'vue';
import { sendData } from "@/utils/fetchUtils";

// "#63e2b7" 成功按下
// "" 无关按键
// 正确按键
// "#e88080" 按错了的按钮

let isActive_Y: any = ref("")
let isActive_U: any = ref("")
let isActive_I: any = ref("")
let isActive_O: any = ref("")
let isActive_P: any = ref("")
let isActive_H: any = ref("")
let isActive_J: any = ref("")
let isActive_K: any = ref("")
let isActive_L: any = ref("")
let isActive_LL: any = ref("")
let isActive_N: any = ref("")
let isActive_M: any = ref("")
let isActive_BB: any = ref("")
let isActive_NN: any = ref("")
let isActive_MM: any = ref("")
let button = [
  "isActive_Y",
  "isActive_U",
  "isActive_I",
  "isActive_O",
  "isActive_P",
  "isActive_H",
  "isActive_J",
  "isActive_K",
  "isActive_L",
  "isActive_LL",
  "isActive_N",
  "isActive_M",
  "isActive_BB",
  "isActive_NN",
  "isActive_MM"
]
// '' 为正确按钮
// true为其他按钮

let isGhost_Y: any = ref(true)
let isGhost_U: any = ref(true)
let isGhost_I: any = ref(true)
let isGhost_O: any = ref(true)
let isGhost_P: any = ref(true)
let isGhost_H: any = ref(true)
let isGhost_J: any = ref(true)
let isGhost_K: any = ref(true)
let isGhost_L: any = ref(true)
let isGhost_LL: any = ref(true)
let isGhost_N: any = ref(true)
let isGhost_M: any = ref(true)
let isGhost_BB: any = ref(true)
let isGhost_NN: any = ref(true)
let isGhost_MM: any = ref(true)
let ghostButton: any = [
  "isGhost_Y",
  "isGhost_U",
  "isGhost_I",
  "isGhost_O",
  "isGhost_P",
  "isGhost_H",
  "isGhost_J",
  "isGhost_K",
  "isGhost_L",
  "isGhost_LL",
  "isGhost_N",
  "isGhost_M",
  "isGhost_BB",
  "isGhost_NN",
  "isGhost_MM"
]
let socket;
let originalSheet = new Set()
let pressedKeys = new Set()


function initWebSocket() {

  const socket = new WebSocket('ws://127.0.0.1:11451');
  debugger
  // 添加 WebSocket 事件监听
  socket.onopen = () => {
    console.log('WebSocket 已连接');
  };

  socket.onmessage = (event) => {
    const key = decodeURIComponent(event.data)// 获取按下的按键
    console.log("originalSheet",originalSheet)
    console.log("pressedKeys",pressedKeys)
    console.log("key",key)
    if (originalSheet.has(key)) {
      pressedKeys.add(key); // 添加按键到记录中
      let char = key
      char = char.replace(/\,/g, 'bb');  // 替换 ',' 为 'll'
      char = char.replace(/\;/g, 'll');  // 替换 ';' 为 'bb'
      char = char.replace(/\./g, 'nn'); // 替换 '.' 为 'nn'
      char = char.replace(/\//g, 'mm'); // 替换 '/' 为 'mm'
      eval("isGhost_" + char.toUpperCase() + ".value = ''")

      // 检查是否所有目标按键都按过一次
      if (pressedKeys.size === originalSheet.size) {
        getNextKey(true)

      }
    } else {
      // getNextKey(false)
    }

  };

  socket.onclose = () => {
    console.log('WebSocket 已断开');
  };

  socket.onerror = (error) => {
    console.error('WebSocket 出现错误', error);
  };
}
initWebSocket()

function logout() {
  // 检查连接状态
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close();
  }
  // 清理状态
  socket = null;
}
window.addEventListener('beforeunload', logout);



function getNextKey(pass) {
  // 重置所有状态
  ghostButton.forEach(char => eval(char + ".value = true"))
  button.forEach(char => eval(char + ".value = ''"))
  originalSheet.clear()
  pressedKeys.clear()

  // 获取新按键
  sendData("nextSheet", {
    type: (pass ? 'ok' : '不ok')
  }).then(res => {
    ghostButton.forEach(char => eval(char + ".value = true"))
    console.log("giao", res)
    let array = res.split('')
    array.forEach(char => {
      char = char.replace(/\,/g, 'bb');  // 替换 ',' 为 'll'
      char = char.replace(/\;/g, 'll');  // 替换 ';' 为 'bb'
      char = char.replace(/\./g, 'nn'); // 替换 '.' 为 'nn'
      char = char.replace(/\//g, 'mm'); // 替换 '/' 为 'mm'
      eval("isGhost_" + char.toUpperCase() + ".value = ''")
    });
    originalSheet = new Set(array)
    pressedKeys = new Set()
  })
}
getNextKey(false)

</script>