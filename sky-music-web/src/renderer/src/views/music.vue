<template>
  <n-flex align="center">
    <n-gradient-text :size="20" type="success" style="width: 100%">
      {{ '当前播放: ' + nowPlayMusic + '' }}
      <br />
      <n-progress style="max-width: 60%; display: inline-block" type="line" :percentage="progress"
        indicator-placement="inside" processing :color="{ stops: ['white', 'blue'] }" @click="progressClick" />
    </n-gradient-text>
    <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('pre')">
      <template #icon>
        <n-icon><PlaySkipBack /></n-icon>
      </template>
    </n-button>
    <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('resume')" v-show="!isPlay" >
      <template #icon>
        <n-icon><Play /></n-icon>
      </template>
    </n-button>
    <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('pause')" v-show="isPlay" >
      <template #icon>
        <n-icon><Pause /></n-icon>
      </template>
    </n-button>
    <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('next')">
      <template #icon>
        <n-icon><PlaySkipForward /></n-icon>
      </template>
    </n-button>
    <n-button quaternary circle type="info" size="large" @click="musicList()">
      <template #icon>
        <n-icon><List /></n-icon>
      </template>
    </n-button>
    <n-switch size="medium" v-model:value="isRandom">
      <template #checked-icon>
        <n-icon :component="ShuffleOutline" />
      </template>
      <template #unchecked-icon>
        <n-icon :component="List" />
      </template>
    </n-switch>
    <n-upload action="http://localhost:9899/userMusicUpload" multiple style="width: 100px; height: 34px" accept=".txt"
      :show-file-list="false" @finish="handleFinish" @before-upload="beforeFileUpload">
      <n-button type="info" ghost> 选择乐谱📯 </n-button>
    </n-upload>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13"> 间隔延迟s&nbsp;&nbsp;&nbsp; </n-gradient-text>
        <n-radio-group v-model:value="delayStatus" name="radiogroup">
          <n-space>
            <n-radio key="system" value="system">系统自带</n-radio>
            <n-radio key="random" value="random">随机</n-radio>
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col v-show="delayStatus == 'custom'" :span="9" style="margin-left: -50px">
        <n-input-number v-model:value="delaySpeed" size="tiny" :min="0" :max="2"  placeholder="输入间隔延迟" />
      </n-col>
    </n-row>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13"> 延音设置s&nbsp;&nbsp;&nbsp; </n-gradient-text>
        <n-radio-group v-model:value="sustainStatus" name="radiogroup">
          <n-space>
            <n-radio key="system" value="system">系统自带</n-radio>
            <n-radio key="random" value="random">随机</n-radio>
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col v-show="sustainStatus == 'custom'" :span="9" style="margin-left: -50px">
        <n-input-number v-model:value="sustainSpeed" size="tiny" :min="0" :max="2" placeholder="输入延音持续" />
      </n-col>
    </n-row>
    <n-row gutter="12">
      <n-col :span="3">
        <n-gradient-text type="info" :size="13"> 倍速设置-&nbsp;&nbsp;&nbsp; </n-gradient-text>
      </n-col>
      <n-col :span="0" style="margin-left: -1.2%">
        <n-input-number v-model:value="playSpeed" size="tiny" :min="0.25" :max="5" placeholder="输入倍速速度" />
      </n-col>
    </n-row>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13"> 播放延迟s&nbsp;&nbsp;&nbsp; </n-gradient-text>
        <n-radio-group v-model:value="playDelayStatus" name="radiogroup">
          <n-space>
            <n-radio key="system" value="system">无</n-radio>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col v-show="playDelayStatus == 'custom'" :span="9" style="margin-left: -50px">
        <n-space vertical style="width: 150px; float: right; margin-top: 2px">
          <n-slider v-model:value="playDelay" :step="1" :min="1" :max="10" />
        </n-space>
      </n-col>
    </n-row>
  </n-flex>
  <n-card style="margin-top: 15px">
    <n-tabs type="bar" animated size="small" @update:value="handleUpdateValue" @before-leave="handleBeforeLeave">
      <n-tab-pane name="systemMusic" tab="自带歌曲">
        <n-data-table :columns="musicColumns" :data="music.systemMusic" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.systemMusic?.length > 7" :row-props="MusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myImport" tab="导入歌曲">
        <n-data-table :columns="myImportColumns" :data="music.myImport" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.myImport?.length > 7" :row-props="MusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="转换歌曲">
        <n-data-table :columns="musicColumns" :data="music.myTranslate" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.myTranslate?.length > 7" :row-props="MusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myFavorite" tab="收藏">
        <n-data-table :columns="favoritColumns" :data="music.myFavorite" :bordered="false" :min-row-height="48"
          :max-height="300" :virtual-scroll="music.myFavorite?.length > 7" :row-props="MusicSelect" />
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
</template>

<script lang="ts" setup>
import { getData, sendData, getList, setConfig } from '@renderer/utils/fetchUtils'
import { RowData } from 'naive-ui/es/data-table/src/interface'
import { h, onUnmounted, reactive, ref, watch } from 'vue'
import { NButton, useMessage } from 'naive-ui'
import { 
  Search,
  ShuffleOutline,
  List,
  Play,
  PlaySkipForward,
  PlaySkipBack,
  Pause
  } from '@vicons/ionicons5'
const message = useMessage()
const music: any = reactive({
  // 音乐列表
  systemMusic: [], // 原版音乐
  myImport: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
  myFavorite: [] // 我的最爱
})
const nowPlayMusic = ref('没有歌曲') // 当前选中歌曲
let nowType = 'systemMusic'
let progressInterval: any = 0
let socket
const searchText = ref('')
const nowState:any = ref('stop') // 当前播放状态
const delayStatus = ref('system')
const sustainStatus = ref('system')
const playDelayStatus = ref('system')
const isRandom = ref(false)
const isPlay = ref(false)
const musicColumns = [
  {
    title: '歌名',
    key: 'name',
    resizable: true
  },
  {
    title: '操作',
    key: 'operation',
    width: 100,
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
    resizable: true
  },
  {
    title: '操作',
    key: 'operation',
    width: 100,
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
    resizable: true
  },
  {
    title: '操作',
    key: 'operation',
    width: 100,
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

const progress = ref(0.0) // 播放进度条
const playSpeed = ref(1) // 播放速度
const delaySpeed = ref(0) // 延迟设置
const sustainSpeed = ref(0) // 延音设置
const playDelay = ref(0) // 播放延迟


let clickTimeout: any = null;
const MusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      if (clickTimeout) {
        clearTimeout(clickTimeout);
        clickTimeout = null;
        progress.value = 0;
        setTimeout(() => {
          sendData('start', {
            fileName: nowPlayMusic.value,
            type: nowType
          });
          isPlay.value = true;
          message.success('开始');
          progressInterval = setInterval(getProgress, 1000);
        }, playDelay.value * 1000);
      } else {
          nowPlayMusic.value = row.name;
          clickTimeout = setTimeout(() => {
            clickTimeout = null;
          }, 300);
      }
    }
  }
};

const playBarClickHandler = (status: String) =>{
  if(status === 'resume'){
    if(nowState.value == 'stop')  {
        message.info("双击歌曲播放！")
        return
    }
    getData('resume')
    isPlay.value = true;
    progressInterval = setInterval(getProgress, 1000)
  }
  if(status === 'pause'){
    getData('pause')
    isPlay.value = false;
    clearInterval(progressInterval)
    progressInterval = 0
  }
  if(status === 'stop'){
    getData('stop')
    clearPlayInfo()
  }
  if(status === 'start'){
      setTimeout(() => {
        sendData('start', {
          fileName: nowPlayMusic.value,
          type: nowType
        })
        message.success('开始')
        isPlay.value = true;
        progressInterval = setInterval(getProgress, 1000)
      }, playDelay.value * 1000)
  }
  if(status === 'pre'){
    return
  }
  if(status === 'next'){
    return
  }
  nowState.value = status
}

const musicList = () =>{

}

function progressClick(event) {
  if (nowState.value === 'stop') {
    message.error('没有歌曲在播放，请播放歌曲后继续操作')
    return
  }
  // 获取点击事件对象
  const rect = event.currentTarget.getBoundingClientRect() // 获取组件的边界框
  const clickPosition = event.clientX - rect.left // 计算点击位置（相对于组件左边）
  const componentWidth = rect.width // 获取组件的总宽度
  // 计算百分比
  const percentage = (clickPosition / componentWidth) * 100
  // 更新进度条
  progress.value = parseFloat(Math.min(Math.max(percentage, 0), 100).toFixed(1)) // 限制在0-100之间
  setConfig('set_progress', progress.value / 100)
}

function getProgress() {
  getData('getProgress').then((res) => {
    progress.value = res.now_progress
  })
  if (progress.value == 100) 
    if(isRandom.value){
      getData('stop')
      clearPlayInfo()
      randomMusicSelect()
    }else{
    }
}
function randomMusicSelect(){
  getData('stop').then(()=>{
    clearPlayInfo()
    nowPlayMusic.value =  music.systemMusic[Math.floor(Math.random() * (music.systemMusic.length))].name
    progress.value = 0
  })
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
      setConfig('delay_interval', 0.01)
      clearInterval(randomInterval)
      break
    case 'random':
      randomInterval = setInterval(() => {
        setConfig('delay_interval', (Math.random() * (0.06 - 0.01) + 0.01).toFixed(3))
      }, 1000)
      break
    case 'custom':
      setConfig('delay_interval', delaySpeed.value)
      clearInterval(randomInterval)
      break
  }
})

let sustainInterval: any = null
watch(sustainStatus, () => {
  switch (sustainStatus.value) {
    case 'system':
      setConfig('sustain_time', 0.01)
      clearInterval(sustainInterval)
      break
    case 'random':
      sustainInterval = setInterval(() => {
        setConfig('sustain_time', (Math.random() * (0.6 - 0.02) + 0.02).toFixed(3))
      }, 1000)
      break
    case 'custom':
      setConfig('sustain_time', sustainSpeed.value)
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

function clearPlayInfo() {
  nowPlayMusic.value = '没有歌曲'
  nowState.value = 'stop'
  progress.value = 0
  clearInterval(progressInterval)
  statusbar[0] = true
  statusbar[1] = false
  isPlay.value = false;
}

//  收藏点击
function heartClick(name, state) {
  if (state) {
    sendData('setFavoriteMusic', {
      fileName: name,
      type: nowType
    }).then(() => {
      handleUpdateValue('myFavorite')
      handleUpdateValue('systemMusic')
      handleUpdateValue('myImport')
      handleUpdateValue('myTranslate')
      message.success('收藏成功')
    })
  } else {
    sendData('dropFile', {
      fileName: name,
      type: 'myFavorite'
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
  sendData('dropFile', {
    fileName: name,
    type: 'myImport'
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
    if(key === 'F5'){
      if (nowState.value != 'stop') {
        window.api.system_notification("🍎", "仅停止状态下允许开始")
      } else {
        console.log("else")
        if (nowPlayMusic.value === '没有歌曲') {
          window.api.system_notification("😭", "选个歌再播放吧靓仔")
        }else{
          window.api.system_notification("✔", "开始")
          playBarClickHandler('start')
        }
      }
    }
    if(key === 'F6'){
      if (nowState.value === 'pause') {
          window.api.system_notification("▶", "继续")
          playBarClickHandler('resume')
      }else{
        window.api.system_notification("🍎", "仅暂停状态下允许继续")
      }
    }
    if(key === 'F7'){
      if (isPlay.value) {
        window.api.system_notification("⏸", "暂停")
        playBarClickHandler('pause')
      }else{
        window.api.system_notification("🍎", "仅正在播放时允许暂停")
      }
    }
    if(key === 'F8'){
      window.api.system_notification("🛑", "停止")
      playBarClickHandler('stop')
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
onUnmounted(() => {
  if (socket) {
    socket.close()
    socket = null
    getData('stop')
    clearPlayInfo()
  }
})
</script>
