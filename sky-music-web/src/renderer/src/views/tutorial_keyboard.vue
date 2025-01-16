<template>
  <div id="father">
    <n-space style="width: 100%;" align='center' justify='center'>
      <n-button
        class="buttonStyle"
        :type="isGhost_Y ? '' : 'primary'"
        :ghost="isGhost_Y"
        :style="!isGhost_Y ? '--n-border: 3px solid #63e2b7' : null"
        >Y</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_U ? '' : 'primary'"
        :ghost="isGhost_U"
        :style="!isGhost_U ? '--n-border: 3px solid #63e2b7' : null"
        >U</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_I ? '' : 'primary'"
        :ghost="isGhost_I"
        :style="!isGhost_I ? '--n-border: 3px solid #63e2b7' : null"
        >I</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_O ? '' : 'primary'"
        :ghost="isGhost_O"
        :style="!isGhost_O ? '--n-border: 3px solid #63e2b7' : null"
        >O</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_P ? '' : 'primary'"
        :ghost="isGhost_P"
        :style="!isGhost_P ? '--n-border: 3px solid #63e2b7' : null"
        >P</n-button
      >
    </n-space>
    <n-space class="dynamicSpaceStyles" align='center' justify='center'>
      <n-button 
        class="buttonStyle"
        :type="isGhost_H ? '' : 'primary'"
        :ghost="isGhost_H"
        :style="!isGhost_H ? '--n-border: 3px solid #63e2b7' : null"
        >H</n-button
      >
      <n-button 
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_J ? '' : 'primary'"
        :ghost="isGhost_J"
        :style="!isGhost_J ? '--n-border: 3px solid #63e2b7' : null"
        >J</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_K ? '' : 'primary'"
        :ghost="isGhost_K"
        :style="!isGhost_K ? '--n-border: 3px solid #63e2b7' : null"
        >K</n-button
      >
      <n-button 
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_L ? '' : 'primary'"
        :ghost="isGhost_L"
        :style="!isGhost_L ? '--n-border: 3px solid #63e2b7' : null"
        >L</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_LL ? '' : 'primary'"
        :ghost="isGhost_LL"
        :style="!isGhost_LL ? '--n-border: 3px solid #63e2b7' : null"
        >;</n-button
      >
    </n-space>
    <n-space class="dynamicSpaceStyles" align='center' justify='center'>
      <n-button
        class="buttonStyle"
        :type="isGhost_N ? '' : 'primary'"
        :ghost="isGhost_N"
        :style="!isGhost_N ? '--n-border: 3px solid #63e2b7' : null"
        >N</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_M ? '' : 'primary'"
        :ghost="isGhost_M"
        :style="!isGhost_M ? '--n-border: 3px solid #63e2b7' : null"
        >M</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle" 
        :type="isGhost_BB ? '' : 'primary'"
        :ghost="isGhost_BB"
        :style="!isGhost_BB ? '--n-border: 3px solid #63e2b7' : null"
        >,</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_NN ? '' : 'primary'"
        :ghost="isGhost_NN"
        :style="!isGhost_NN ? '--n-border: 3px solid #63e2b7' : null"
        >.</n-button
      >
      <n-button
        class="dynamicButtonStyles buttonStyle"
        :type="isGhost_MM ? '' : 'primary'"
        :ghost="isGhost_MM"
        :style="!isGhost_MM ? '--n-border: 3px solid #63e2b7' : null"
        >/</n-button
      >
    </n-space>
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref } from 'vue'
import { sendData } from '@renderer/utils/fetchUtils'
const isGhost_Y: any = ref(true)
const isGhost_U: any = ref(true)
const isGhost_I: any = ref(true)
const isGhost_O: any = ref(true)
const isGhost_P: any = ref(true)
const isGhost_H: any = ref(true)
const isGhost_J: any = ref(true)
const isGhost_K: any = ref(true)
const isGhost_L: any = ref(true)
const isGhost_LL: any = ref(true)
const isGhost_N: any = ref(true)
const isGhost_M: any = ref(true)
const isGhost_BB: any = ref(true)
const isGhost_NN: any = ref(true)
const isGhost_MM: any = ref(true)
const ghostButton: any = [
  'isGhost_Y',
  'isGhost_U',
  'isGhost_I',
  'isGhost_O',
  'isGhost_P',
  'isGhost_H',
  'isGhost_J',
  'isGhost_K',
  'isGhost_L',
  'isGhost_LL',
  'isGhost_N',
  'isGhost_M',
  'isGhost_BB',
  'isGhost_NN',
  'isGhost_MM'
]
let socket
let originalSheet = new Set()
let pressedKeys = new Set()

function initWebSocket() {
  socket = new WebSocket('ws://127.0.0.1:11451')
  // 添加 WebSocket 事件监听
  socket.onopen = () => {
    console.log('WebSocket 已连接')
  }

  socket.onmessage = (event) => {
    const key = decodeURIComponent(event.data) // 获取按下的按键
    console.log('originalSheet', originalSheet)
    console.log('pressedKeys', pressedKeys)
    console.log('key', key)
    if (originalSheet.has(key)) {
      pressedKeys.add(key) // 添加按键到记录中
      let char = key
      char = char.replace(/\,/g, 'bb') // 替换 ',' 为 'll'
      char = char.replace(/\;/g, 'll') // 替换 ';' 为 'bb'
      char = char.replace(/\./g, 'nn') // 替换 '.' 为 'nn'
      char = char.replace(/\//g, 'mm') // 替换 '/' 为 'mm'
      eval('isGhost_' + char.toUpperCase() + ".value = ''")

      // 检查是否所有目标按键都按过一次
      if (pressedKeys.size === originalSheet.size) {
        getNextKey(true)
      }
    } else {
      // getNextKey(false)
    }
  }

  socket.onclose = () => {
    console.log('WebSocket 已断开')
  }

  socket.onerror = (error) => {
    console.error('WebSocket 出现错误', error)
  }
}
initWebSocket()

function logout() {
  // 检查连接状态
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close()
  }
  // 清理状态
  socket = null
}
window.addEventListener('beforeunload', logout)

function getNextKey(pass) {
  // 重置所有状态
  ghostButton.forEach((char) => eval(char + '.value = true'))
  originalSheet.clear()
  pressedKeys.clear()

  // 获取新按键
  sendData('follow', {
    type: pass ? 'ok' : '不ok',
    operate: 'nextSheet'
  }).then((res) => {
    ghostButton.forEach((char) => eval(char + '.value = true'))
    console.log('giao', res)
    const array = res.split('')
    array.forEach((char) => {
      char = char.replace(/\,/g, 'bb') // 替换 ',' 为 'll'
      char = char.replace(/\;/g, 'll') // 替换 ';' 为 'bb'
      char = char.replace(/\./g, 'nn') // 替换 '.' 为 'nn'
      char = char.replace(/\//g, 'mm') // 替换 '/' 为 'mm'
      eval('isGhost_' + char.toUpperCase() + ".value = ''")
    })
    originalSheet = new Set(array)
    pressedKeys = new Set()
  })
}
getNextKey(false)

//  记录上一次坐标如果改动了才进行识别，节约资源
let last_x = 0
let last_y = 0
let last_width = 0
let last_height = 0
let moveInterval:any = null
onMounted(() => {
  setInterval(()=>{
    sendData("config_operate",{
        operate: 'game_position'
      }).then(res=>{
          const [x, y, x2, y2] = res;
          const width = x2 - x;
          const height = (y2 - y) * 0.7;
          // 直接设置窗口大小和位置
          if(x === last_x && y === last_y && x2 === last_width && y2 === last_height){
            sendData("config_operate",{
              operate: 'get_key_position',
              conf: 0.85
            }).then(postions=>{
              console.log(postions)
            })
          }else{
            window.electron.setFollowWindow(x, y, width, height);
            last_x = x
            last_y = y
            last_width = x2
            last_height = y2
          }
      })
  },1000)
})

onUnmounted(() => {
  clearInterval(moveInterval)
})

</script>

<style scoped>
*{
  transition: 0.3s; /* 平滑过渡效果 */
}
#father {
  /* 带menu 289 不带315 */
  /* height: 289px; */
  height: 100vh;
  justify-content: center;
  align-content: center;
}
.buttonStyle{
    height: 84px;
    width: 84px;
    font-size: 25px;
}

.dynamicButtonStyles{
    margin-left: 18px;
}
.dynamicSpaceStyles{
  margin-top: 35px;
}

</style>
