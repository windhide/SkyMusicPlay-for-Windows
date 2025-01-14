<template>
  <n-flex align="center">
    <n-gradient-text :size="20" type="success" style="width: 100%; color:#F2C9C4">
      {{ '播&nbsp&nbsp&nbsp放: ' + nowPlayMusic + '' }}
    </n-gradient-text>
    <n-gradient-text :size="20" type="success" style="width: 100%; color:#F2E8C4">
      {{ '选&nbsp&nbsp&nbsp择: ' + nowSelectMusic + '' }}
    </n-gradient-text>
      <n-slider v-model:value="progress" :step="0.1" style="max-width: 51.5%; display: inline-block; margin-left: 3px;" 
        @dragend="drag_progress_end" @dragstart="drag_progress_start">
        <template #thumb>
          <n-icon-wrapper :size="20" :border-radius="12" style="background-color:#F2E8C4">
            <n-icon :size="16" :component="PawSharp" />
          </n-icon-wrapper>
        </template>
      </n-slider>
    <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('resume', '')" v-show="!isPlay" color="#F2C9C4">
      <template #icon>
        <n-icon>
          <Play />
        </n-icon>
      </template>
    </n-button>
    <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('pause', '')" v-show="isPlay" color="#F2C9C4">
      <template #icon>
        <n-icon>
          <Pause />
        </n-icon>
      </template>
    </n-button>
    <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('next', '')" color="#F2C9C4">
      <template #icon>
        <n-icon>
          <PlaySkipForward />
        </n-icon>
      </template>
    </n-button>
    <n-button quaternary circle type="info" size="large" @click="reloadMusicList()" color="#F2C9C4">
      <template #icon>
        <n-icon>
          <SparklesOutline />
        </n-icon>
      </template>
    </n-button>
    <n-popselect v-model:value="selectMode" :options="modeColumns">
      <n-button circle dashed color="#F2C9C4">
        <template #icon>
          <n-icon v-if="selectMode == 'order'"><List /></n-icon>
          <n-icon v-if="selectMode == 'random'"><ShuffleOutline /></n-icon>
          <n-icon v-if="selectMode == 'cycle'"><Sync /></n-icon>
        </template>
      </n-button>
    </n-popselect>
    <n-upload action="http://localhost:9899/userMusicUpload" multiple accept=".txt" style="width: 20px; margin-left: 8px;"
      :show-file-list="false" @finish="handleFinish" @before-upload="beforeFileUpload">
      <n-button type="info" ghost circle dashed color="#F2C9C4">
        <template #icon>
          <n-icon><CloudUploadOutline /></n-icon>
        </template>
      </n-button>
    </n-upload>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13" style="color: #F2C9C4"> 间隔延迟s&nbsp;&nbsp;&nbsp; </n-gradient-text>
        <n-radio-group v-model:value="delayStatus" name="radiogroup">
          <n-space>
            <n-radio key="system" value="system" style="color: red;">系统自带</n-radio>
            <n-radio key="random" value="random">随机</n-radio>
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col v-show="delayStatus == 'custom'" :span="9" style="margin-left: -50px">
        <n-input-number step="0.01" v-model:value="delaySpeed" size="tiny" :min="0" :max="2" placeholder="输入间隔延迟" />
      </n-col>
    </n-row>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13" style="color: #F2C9C4"> 延音设置s&nbsp;&nbsp;&nbsp; </n-gradient-text>
        <n-radio-group v-model:value="sustainStatus" name="radiogroup">
          <n-space>
            <n-radio key="system" value="system">系统自带</n-radio>
            <n-radio key="random" value="random">随机</n-radio>
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col v-show="sustainStatus == 'custom'" :span="9" style="margin-left: -50px">
        <n-input-number step="0.01" v-model:value="sustainSpeed" size="tiny" :min="0" :max="2" placeholder="输入延音持续" />
      </n-col>
    </n-row>
    <n-row gutter="12">
      <n-col :span="3">
        <n-gradient-text type="info" :size="13" style="color: #F2C9C4"> 倍速设置-&nbsp;&nbsp;&nbsp; </n-gradient-text>
      </n-col>
      <n-col :span="0" style="margin-left: -1.2%">
        <n-input-number step="0.1" v-model:value="playSpeed" size="tiny" :min="0.25" :max="5" placeholder="输入倍速速度" />
      </n-col>
    </n-row>
  </n-flex>
  <n-card style="margin-top: 15px;">
    <n-tabs type="bar" animated size="small" @update:value="handleUpdateValue" @before-leave="handleBeforeLeave">
      <n-tab-pane name="systemMusic" tab="自带歌曲">
        <n-data-table :columns="musicColumns" :data="music.systemMusic" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.systemMusic?.length > 7" :row-props="MusicSelect" row-class-name="td_css" />
      </n-tab-pane>
      <n-tab-pane name="myImport" tab="导入歌曲">
        <n-data-table :columns="myImportColumns" :data="music.myImport" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.myImport?.length > 7" :row-props="MusicSelect"  row-class-name="td_css" />
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="转换歌曲">
        <n-data-table :columns="musicColumns" :data="music.myTranslate" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.myTranslate?.length > 7" :row-props="MusicSelect" row-class-name="td_css"  />
      </n-tab-pane>
      <n-tab-pane name="myFavorite" tab="收藏">
        <n-data-table :columns="favoritColumns" :data="music.myFavorite" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.myFavorite?.length > 7" :row-props="MusicSelect"  row-class-name="td_css" />
      </n-tab-pane>
      <template #suffix>
        <n-input v-model:value="searchText" round placeholder="搜索"
          style="margin-bottom: 5px; width: 25vh; margin-left: 5px">
          <template #suffix>
            <n-icon :component="Search" />
          </template>
        </n-input>
      </template>
    </n-tabs>
  </n-card>
  <n-drawer v-model:show="active" :width="400" :placement="placement" style="border-radius: 30px;">
    <n-drawer-content title="播放列表">
      <n-button type="info" ghost style="margin-bottom: 10px;" @click="clearPlayList" color="#F2C9C4"> 清空 </n-button>
      <n-data-table :columns="musicListColumns" :max-height="570" :data="music.musicList" :bordered="false"
        :height-for-row="1" :virtual-scroll="music.systemMusic?.length > 7" :row-props="musicListSelect" />
    </n-drawer-content>
  </n-drawer>
</template>


<script lang="ts" setup>
import { getData, sendData, getList, setConfig } from '@renderer/utils/fetchUtils'

import { RowData } from 'naive-ui/es/data-table/src/interface'
import { h, onUnmounted, reactive, ref, watch } from 'vue'
import { NButton, useMessage, DrawerPlacement } from 'naive-ui'
import {
  Search,
  ShuffleOutline,
  List,
  Play,
  PlaySkipForward,
  Pause,
  PawSharp,
  Sync,
  SparklesOutline,
  CloudUploadOutline
} from '@vicons/ionicons5'
import { useStore } from 'vuex'
const message = useMessage()
const music: any = reactive({
  // 音乐列表
  systemMusic: [], // 原版音乐
  myImport: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
  myFavorite: [], // 我的最爱
  musicList: [] // 我的最爱
})
const nowSelectMusic = ref('没有歌曲') // 当前选中歌曲
const nowPlayMusic = ref('没有歌曲') // 当前选中歌曲
let nowType = 'systemMusic'
let progressInterval: any = 0
let socket
const searchText = ref('')
const nowState: any = ref('stop') // 当前播放状态
const delayStatus = ref('system')
const sustainStatus = ref('system')
const isPlay = ref(false)
const active = ref(false)
const placement = ref<DrawerPlacement>('left')
const store = useStore()
const selectMode = ref("order")
let cycleMusic:any = {}
const modeColumns = [
  {
    label: '顺序',
    value: 'order'
  },
  {
    label: '随机',
    value: 'random'
  },
  {
    label: '循环',
    value: 'cycle'
  }
]
const musicColumns = [
  {
    title: '歌名',
    key: 'name',
    resizable: true,
    className: 'th_css'
  },
  {
    title: '操作',
    key: 'operation',
    width: 100,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text:
            music.myFavorite.filter((res) => {
              return res.name.replaceAll('.mp3').includes(row.name)
            }).length == 0
              ? false
              : true,
          onClick: () => heartClick(row.name, true)
        },
        {
          default: () => {
            return music.myFavorite.filter((res) => {
              return res.name.replaceAll('.mp3').includes(row.name)
            }).length == 0
              ? '❤'
              : null
          }
        }
      )
    }
  }
] // 音乐列

const favoritColumns = [
  {
    title: '歌名',
    key: 'name',
    resizable: true,
    className: 'th_css'
  },
  {
    title: '操作',
    key: 'operation',
    width: 100,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text: false,
          onClick: () => heartClick(row.name, false)
        },
        {
          default: () => {
            return '💔'
          }
        }
      )
    }
  }
] // 音乐列

const myImportColumns = [
  {
    title: '歌名',
    key: 'name',
    resizable: true,
    className: 'th_css'
  },
  {
    title: '操作',
    key: 'operation',
    width: 100,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text: false,
          onClick: () => deleteClick(row.name)
        },
        {
          default: () => {
            return '❌'
          }
        }
      )
    }
  }
] // 音乐列

const musicListColumns = [
  {
    title: '歌名',
    key: 'name',
    resizable: true,
    className: 'th_css'
  }
] // 音乐列

const progress = ref(0.0) // 播放进度条
const playSpeed = ref(1) // 播放速度
const delaySpeed: any = ref(0.01) // 延迟设置
const sustainSpeed: any = ref(0.01) // 延音设置


let clickTimeout: any = null;
const MusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      if (clickTimeout) {
        clearTimeout(clickTimeout);
        clickTimeout = null;
        playBarClickHandler("start", "")
      } else {
        nowSelectMusic.value = row.name;
        clickTimeout = setTimeout(() => {
          clickTimeout = null;
          store.commit('addPlayList', { 'name': row.name, 'type': nowType });
        }, 300);
      }
    }
  }
};

const musicListSelect = (row: RowData, rowIndex: number) => {
  console.log(row)
  return {
    onClick: () => {
      store.commit("removePlayList", rowIndex)
      music.musicList = store.getters.getPlayList
    }
  }
};

function reloadMusicList() {
  active.value = !active.value;
  music.musicList = store.getters.getPlayList
}
function clearPlayList() {
  store.commit('clearPlayList')
  music.musicList = store.getters.getPlayList
}

const playBarClickHandler = async (status: String, type: String) => {
  if (status === 'resume') {
    if (nowState.value == 'stop') {
      message.info("双击歌曲播放！")
      return
    }
    sendData('play_operate',{"operate":"resume"})
    isPlay.value = true;
    progressInterval = setInterval(getProgress, 1000)
  }
  if (status === 'pause') {
    sendData('play_operate',{"operate":"pause"})
    isPlay.value = false;
    clearInterval(progressInterval)
    progressInterval = 0
  }
  if (status === 'stop') {
    sendData('play_operate',{"operate":"stop"})
    await clearPlayInfo()
  }
  if (status === 'start') {
    setTimeout(() => {
      sendData('play_operate', {
        fileName: nowSelectMusic.value,
        type: type != "" ? type : nowType,
        operate: "start"
      }).then(()=>{
        progress.value = 0
        cycleMusic = {
          fileName: nowSelectMusic.value,
          type: type != "" ? type : nowType,
        }
      })
      message.success('开始')
      isPlay.value = true;
      progressInterval = setInterval(getProgress, 1000)
    })
  }
  if (status === 'next') {
    progress.value = 100
    return
  }
  nowState.value = status
}

function drag_progress_start() {
  sendData('play_operate',{"operate":"pause"}).then(() => {
    clearInterval(progressInterval)
  })

}
function drag_progress_end() {
  setConfig('set_progress', progress.value / 100)
  sendData('play_operate',{"operate":"resume"}).then(() => {
    progressInterval = setInterval(getProgress, 1000)
  })
}


async function getProgress() {
  if (progress.value == 100) {
    await clearPlayInfo();
    if (selectMode.value === 'order') orderMusicPlay();
    else if (selectMode.value === 'random') randomMusicPlay();
    else if (selectMode.value === 'cycle') cycleMusicPlay();
  }
  getData('getProgress').then((res) => {
    progress.value = Number(res.now_progress)
    nowPlayMusic.value = res.now_play_music
  })
  return "ok"
}


function randomMusicPlay() {
  nowSelectMusic.value = music.systemMusic[Math.floor(Math.random() * (music.systemMusic.length))].name
  playBarClickHandler("start", 'systemMusic')
  
}

async function orderMusicPlay() {
  let struct = store.getters.getNextPlayMusic
  if (struct != null && struct != undefined) {
    nowSelectMusic.value = struct.name
    let type = struct.type
    playBarClickHandler("start", type)
  } else {
    playBarClickHandler("stop","")
    window.api.system_notification("😳", "列表的歌放完咯")
    nowPlayMusic.value = "没有正在播放的歌曲哦"
  }
}

function cycleMusicPlay() {
  nowSelectMusic.value = cycleMusic?.fileName
  playBarClickHandler("start", cycleMusic?.type)
}

handleUpdateValue('myFavorite')
handleUpdateValue('systemMusic')

function handleUpdateValue(value: string) {
  searchText.value = ''
  getListData(value)
}

function handleBeforeLeave(name: string) {
  nowType = name
  return true
}

watch(searchText, () => {
  getListData('myFavorite')
  getListData('systemMusic')
  getListData('myImport')
  getListData('myTranslate')
})

let randomInterval: any = null
watch(delayStatus, () => {
  switch (delayStatus.value) {
    case 'system':
      delaySpeed.value = 0
      clearInterval(randomInterval)
      break
    case 'random':
      randomInterval = setInterval(() => {
        delaySpeed.value = (Math.random() * (0.06 - 0.01) + 0.01).toFixed(3)
      }, 1000)
      break
    case 'custom':
      delaySpeed.value = 0.01
      clearInterval(randomInterval)
      break
  }
})

let sustainInterval: any = null
watch(sustainStatus, () => {
  switch (sustainStatus.value) {
    case 'system':
      sustainSpeed.value = 0.01
      clearInterval(sustainInterval)
      break
    case 'random':
      sustainInterval = setInterval(() => {
        sustainSpeed.value = (Math.random() * (1.5 - 0.5) + 0.5).toFixed(3)
      }, 1000)
      break
    case 'custom':
      clearInterval(sustainInterval)
      break
  }
})

watch(delaySpeed, () => {
  setConfig('delay_interval', delaySpeed.value)
})
watch(sustainSpeed, () => {
  setConfig('sustain_time', sustainSpeed.value)
})

watch(playSpeed, () => {
  setConfig('play_speed', playSpeed.value)
})

async function clearPlayInfo() {
  await clearInterval(progressInterval)
  nowSelectMusic.value = '没有歌曲'
  nowPlayMusic.value = "没有正在播放的歌曲哦"
  nowState.value = 'stop'
  progress.value = 0
  statusbar[0] = true
  statusbar[1] = false
  isPlay.value = false;
}

//  收藏点击
function heartClick(name, state) {
  if (state) {
    sendData('config_operate', {
      fileName: name,
      type: nowType,
      operate: 'favorite_music'
    }).then(() => {
      handleUpdateValue('myFavorite')
      handleUpdateValue('systemMusic')
      handleUpdateValue('myImport')
      handleUpdateValue('myTranslate')
      message.success('收藏成功')
    })
  } else {
    sendData('config_operate', {
      fileName: name,
      type: 'myFavorite',
      operate: "drop_file"
    }).then(() => {
      handleUpdateValue('myFavorite')
      handleUpdateValue('systemMusic')
      handleUpdateValue('myImport')
      handleUpdateValue('myTranslate')
      message.success('移除成功')
    })
  }
}

// 删除点击
function deleteClick(name) {
  sendData('config_operate', {
    fileName: name,
    type: 'myImport',
    operate: "drop_file"
  }).then(() => {
    handleUpdateValue('myFavorite')
    handleUpdateValue('systemMusic')
    handleUpdateValue('myImport')
    handleUpdateValue('myTranslate')
    message.success('删除成功')
  })
}

function handleFinish({ file: _file, event: _event }) {
  handleUpdateValue('myImport')
}

function beforeFileUpload(file) {
  return window.api.readFile(file.file.file.path).then(res => {
    if (res) {
      message.success("谱子👉" + file.file.file.name + "完成导入")
    } else {
      message.error("谱子👉" + file.file.file.name + "导入失败")
    }
    return res;
  })
}

function getListData(value) {
  getList(value, searchText.value).then((_res) => {
    eval('music.' + value + '=_res')
  })
}

function initWebSocket() {
  socket = new WebSocket('ws://127.0.0.1:11452')
  // 添加 WebSocket 事件监听
  socket.onopen = () => {
    console.log('WebSocket 已连接')
  }
  socket.onmessage = (event) => {
    const key = decodeURIComponent(event.data).trim() // 获取按下的按键
    if (key === 'F5') {
      if (nowState.value != 'stop') {
        window.api.system_notification("🍎", "仅停止状态下允许开始")
      } else {
        console.log("else")
        if (nowSelectMusic.value === '没有歌曲') {
          window.api.system_notification("😭", "选个歌再播放吧靓仔")
        } else {
          window.api.system_notification("✔", "开始")
          playBarClickHandler('start', '')
        }
      }
    }
    if (key === 'F6') {
      if (nowState.value === 'pause') {
        window.api.system_notification("▶", "继续")
        playBarClickHandler('resume', '')
      } else {
        window.api.system_notification("🍎", "仅暂停状态下允许继续")
      }
    }
    if (key === 'F7') {
      if (isPlay.value) {
        window.api.system_notification("⏸", "暂停")
        playBarClickHandler('pause', '')
      } else {
        window.api.system_notification("🍎", "仅正在播放时允许暂停")
      }
    }
    if (key === 'F8') {
      window.api.system_notification("🛑", "停止")
      playBarClickHandler('stop', '')
    }

    if (key === 'F2') {
      window.api.system_notification("⏩", "下一首")
      playBarClickHandler('next', '')
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
onUnmounted(async () => {
  if (socket) {
    socket.close()
    socket = null
    playBarClickHandler("stop","")
    await clearPlayInfo()
  }
})
</script>
<style scoped>
:deep(.n-slider-rail__fill){
  --n-fill-color-hover: rgb(242,232,196) !important;
  background-color: rgb(242,232,196) !important;
}
:deep(.n-radio){
  --n-box-shadow-active: inset 0 0 0 1px rgb(242,232,196)!important;
  --n-box-shadow-focus: inset 0 0 0 1px rgb(242,232,196), 0 0 0 2px rgba(242,232,196, 0.3)!important;
  --n-box-shadow-hover: inset 0 0 0 1px rgb(242,232,196)!important;
  --n-dot-color-active: rgb(242,232,196)!important;
}
:deep(.n-input){
  --n-border-hover: 1px solid rgb(242,232,196)!important;
  --n-border-focus: 1px solid rgb(242,232,196)!important;
  --n-color-focus: rgba(242,232,196,0.1)!important;
}
:deep(.n-tabs-bar){
  --n-bar-color: rgb(242,232,196)!important;
}
:deep(.n-tabs){
    --n-tab-text-color-active: rgb(242,232,196)!important;
    --n-tab-text-color-hover: rgb(242,232,196)!important;
    --n-tab-text-color: rgb(221,242,196)!important;
}
:deep(.n-switch--active){
  --n-rail-color-active: #F2C9C4 !important;
}
.n-input{
  background-color: rgba(24, 24, 28, 0) !important;
  border: 1px solid rgba(242,232,196,0.5);
}
:deep(.td_css td) {
  color: rgb(242,232,196) !important;
}
:deep(.th_css){
  color: rgb(221,242,196) !important;
}
</style>