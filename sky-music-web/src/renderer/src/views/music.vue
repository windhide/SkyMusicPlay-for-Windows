<template>
  <n-flex align="center" style="margin-left: 6px;">
    <n-gradient-text :size="20" type="success" style="width: 100%; color:#F2C9C4">
      {{ t("music.play") + nowPlayMusic + '' }}
    </n-gradient-text>
    <n-gradient-text :size="20" type="success" style="width: 100%; color:#F2E8C4">
      {{ t("music.chose") + nowSelectMusic + '' }}
    </n-gradient-text>
    <n-flex style="width: 100%">
      <n-slider v-model:value="progress" :step="0.1" style="max-width: 51.5%; display: inline-block; margin-left: 3px;"
                @dragend="drag_progress_end" @dragstart="drag_progress_start">
        <template #thumb>
          <n-icon-wrapper :size="20" :border-radius="12" style="background-color:#F2E8C4">
            <n-icon :size="16" :component="PawSharp" />
          </n-icon-wrapper>
        </template>
      </n-slider>
      <div></div>
    <n-gradient-text :size="15" type="success" style="color:#F2E8C4; margin-top: -2px;">
      {{nowCurrentTime}} / {{nowTotalTime}}
    </n-gradient-text>
    </n-flex>
    <n-row gutter="12">
        <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('resume', '')" v-show="!isPlay" color="#F2C9C4">
          <template #icon>
            <n-icon size="25px">
              <Play />
            </n-icon>
          </template>
        </n-button>
        <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('pause', '')" v-show="isPlay" color="#F2C9C4">
          <template #icon>
            <n-icon size="25px">
              <Pause />
            </n-icon>
          </template>
        </n-button>
        <n-button quaternary circle type="info" size="large" @click="playBarClickHandler('next', '')" color="#F2C9C4" class='actionButton'>
          <template #icon>
            <n-icon size="25px">
              <PlaySkipForward />
            </n-icon>
          </template>
        </n-button>
        <n-popover placement="bottom-start" trigger="click" style="width: 450px; --n-color: rgba(47,47,55,1); border-radius: 10px;">
          <template #trigger>
            <n-button quaternary circle type="info" size="large" color="#F2C9C4" class='actionButton'>
              <template #icon>
                <n-icon size="25px">
                  <Settings48Filled />
                </n-icon>
              </template>
            </n-button>
          </template>
          <n-row gutter="26">
            <n-col :span="15">
              <n-gradient-text type="info" :size="13" style="color: #F2C9C4; display: block;">{{t("music.space.title") }}</n-gradient-text>
              <n-radio-group v-model:value="delayStatus" name="radiogroup" style="margin-top: 5px; margin-bottom: 5px" @keydown.stop.prevent>
                <n-space>
                  <n-radio key="system" value="system" style="color: red;" @keydown.stop.prevent>{{t("music.space.chose0") }}</n-radio>
                  <n-radio key="random" value="random" @keydown.stop.prevent>{{t("music.space.chose1") }}</n-radio>
                  <n-radio key="custom" value="custom" @keydown.stop.prevent>{{t("music.space.chose2") }}</n-radio>
                </n-space>
              </n-radio-group>
            </n-col>
            <n-col v-show="delayStatus == 'custom'" :span="5" style="margin-left: -40px; margin-top: 25px;">
              <n-input-number step="0.01" v-model:value="delaySpeed" size="tiny" :min="0" :max="2" :placeholder="t('music.placeholder1')" style="width: 150px;" />
            </n-col>
            <n-col v-show="delayStatus == 'random'" :span="11" style="margin-left: -40px; margin-top: 25px;">
              <n-input-number step="0.01" v-model:value="delayRandomStart" size="tiny" :min="0" :max="2" :placeholder="t('music.placeholder1')" style="width: 83px; float: inline-start;" />
              <span style="margin-left: 9px;">&nbsp;-&nbsp;</span>
              <n-input-number step="0.01" v-model:value="delayRandomEnd" size="tiny" :min="0" :max="2" :placeholder="t('music.placeholder1')" style="width: 83px; float: inline-end;"/>
            </n-col>
          </n-row>
          <n-row gutter="26">
            <n-col :span="15">
              <n-gradient-text type="info" :size="13" style="color: #F2C9C4; display: block;">{{t("music.space.title1") }}</n-gradient-text>
              <n-radio-group v-model:value="durationStatus" name="radiogroup" style="margin-top: 5px; margin-bottom: 5px" @keydown.stop.prevent>
                <n-space>
                  <n-radio key="system" value="system" @keydown.stop.prevent>{{t("music.space.chose0") }}</n-radio>
                  <n-radio key="random" value="random" @keydown.stop.prevent>{{t("music.space.chose1") }}</n-radio>
                  <n-radio key="custom" value="custom" @keydown.stop.prevent>{{t("music.space.chose2") }}</n-radio>
                </n-space>
              </n-radio-group>
            </n-col>
            <n-col v-show="durationStatus == 'custom'" :span="5" style="margin-left: -40px; margin-top: 25px;">
              <n-input-number step="0.01" v-model:value="durationSpeed" size="tiny" :min="0" :max="2" :placeholder="t('music.placeholder2')" style="width: 150px;" />
            </n-col>
            <n-col v-show="durationStatus == 'random'" :span="11" style="margin-left: -40px; margin-top: 25px;">
              <n-input-number step="0.01" v-model:value="durationRandomStart" size="tiny" :min="0" :max="2" :placeholder="t('music.placeholder2')" style="width: 83px; float: inline-start;"  />
              <span style="margin-left: 9px;">&nbsp;-&nbsp;</span>
              <n-input-number step="0.01" v-model:value="durationRandomEnd" size="tiny" :min="0" :max="2" :placeholder="t('music.placeholder2')" style="width: 83px; float: inline-end;"  />
            </n-col>
          </n-row>
          <n-row gutter="12">
            <n-col :span="5">
              <n-gradient-text type="info" :size="13" style="color: #F2C9C4; display: block;">{{t("music.space.mult_speed") }}</n-gradient-text>
              <n-input-number step="0.1" v-model:value="playSpeed" size="tiny" :min="0.1" :max="5" :placeholder="t('music.space.mult_speed')" style="margin-top: 5px;" />
            </n-col>
          </n-row>
        </n-popover>
        <n-button quaternary circle type="info" size="large" @click="reloadMusicList()" color="#F2C9C4" class='actionButton'>
          <template #icon>
            <n-icon size="25px">
              <BookStar24Filled />
            </n-icon>
          </template>
        </n-button>
        <n-popselect v-model:value="selectMode" :options="modeColumns" style="height:100%">
          <n-button quaternary circle color="#F2C9C4" size="large" class='actionButton'>
            <template #icon>
              <n-icon v-if="selectMode == 'order'" size="25px"><List /></n-icon>
              <n-icon v-if="selectMode == 'random'" size="25px"><ShuffleOutline /></n-icon>
              <n-icon v-if="selectMode == 'cycle'" size="25px"><Sync /></n-icon>
            </template>
          </n-button>
        </n-popselect>
        <n-upload action="http://localhost:9899/userMusicUpload" multiple accept=".txt" style="width: 60px;"
          :show-file-list="false" @finish="handleFinish" @before-upload="beforeFileUpload">
          <n-button type="info" quaternary circle  size="large" color="#F2C9C4" class='actionButton'>
            <template #icon>
              <n-icon size="25px"><CloudArrowUp32Filled /></n-icon>
            </template>
          </n-button>
        </n-upload>
        <n-button quaternary circle type="info" size="large" @click="locationNowPlayMusic()" color="#F2C9C4" class='actionButton'>
          <template #icon>
            <n-icon size="25px">
              <Location28Filled />
            </n-icon>
          </template>
        </n-button>
    </n-row>
  </n-flex>
  <n-card style="margin-left: -16px; width: 640px;" :bordered="false">
    <n-tabs type="bar" animated size="small" @update:value="handleUpdateValue" @before-leave="handleBeforeLeave" :value="tabsNumber">
      <n-tab-pane name="systemMusic" :tab="t('tab.systemMusic')">
        <n-data-table :columns="musicColumns" :data="music.systemMusic" :bordered="false" :min-row-height="48" ref="systemMusic"
          :max-height="430" :virtual-scroll="music.systemMusic?.length > 7" :row-props="MusicSelect" :row-class-name="rowClassName"
          style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <n-tab-pane name="myImport" :tab="t('tab.myImport')" ref="myImport">
        <n-data-table :columns="myImportColumns" :data="music.myImport" :bordered="false" :min-row-height="48" ref="myImport"
        :max-height="430" :virtual-scroll="music.myImport?.length > 7" :row-props="MusicSelect"  :row-class-name="rowClassName"
        style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <n-tab-pane name="myTranslate" :tab="t('tab.myTranslate')" ref="myTranslate">
        <n-data-table :columns="musicColumns" :data="music.myTranslate" :bordered="false" :min-row-height="48" ref="myTranslate"
        :max-height="430" :virtual-scroll="music.myTranslate?.length > 7" :row-props="MusicSelect" :row-class-name="rowClassName"
        style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <n-tab-pane name="myFavorite" :tab="t('tab.myFavorite')" ref="myFavorite">
        <n-data-table :columns="favoritColumns" :data="music.myFavorite" :bordered="false" :min-row-height="48" ref="myFavorite"
        :max-height="430" :virtual-scroll="music.myFavorite?.length > 7" :row-props="MusicSelect"  :row-class-name="rowClassName"
        style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <template #suffix>
        <n-input v-model:value="searchText" round placeholder="搜索" clearable
          style="top:-3px;width: 25vh; margin-left: 5px">
          <template #suffix>
            <n-icon :component="Search" />
          </template>
        </n-input>
      </template>
    </n-tabs>
  </n-card>
  <n-drawer v-model:show="active" :width="400" :placement="placement" style="border-radius: 30px;">
    <n-drawer-content :title="t('tab.title')">
      <n-button type="info" ghost style="margin-bottom: 10px;" @click="clearPlayList" color="#F2C9C4"> {{t('tab.clear')}} </n-button>
      <n-data-table :columns="musicListColumns" :max-height="570" :data="music.musicList" :bordered="false"
        :height-for-row="1" :virtual-scroll="music.systemMusic?.length > 7" :row-props="musicListSelect" />
    </n-drawer-content>
  </n-drawer>
</template>


<script lang="ts" setup>
import { getData, sendData, getList, setConfig } from '@renderer/utils/fetchUtils'

import { DataTableInst, RowData } from 'naive-ui/es/data-table/src/interface'
import { h, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { NButton, useMessage, DrawerPlacement } from 'naive-ui'
import {
  Search,
  ShuffleOutline,
  List,
  Play,
  PlaySkipForward,
  Pause,
  PawSharp,
  Sync
} from '@vicons/ionicons5'
import {
  Settings48Filled,
  BookStar24Filled,
  CloudArrowUp32Filled,
  Location28Filled
} from '@vicons/fluent'
import { useStore } from 'vuex'
import { debounce } from 'lodash-es'
import configStore, { CONFIG_TYPE, CONFIG_STATUS_TYPE } from '@renderer/utils/configStore'
import { useI18n } from "vue-i18n";
const { t } = useI18n();
// ---------------------------------------------------
// 响应式状态和常量定义
// ---------------------------------------------------
const message = useMessage()
const store = useStore()

const music: any = reactive({
  // 音乐列表
  systemMusic: [], // 原版音乐
  myImport: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
  myFavorite: [], // 我的最爱
  musicList: [] // 我的最爱
})

const nowSelectMusic = ref(t('controller.no_music')) // 当前选中歌曲
let nowSelectMusicTruth = "" // 当前选中歌曲真实名称
const nowPlayMusic = ref(t('controller.no_music')) // 当前播放歌曲名称
let nowType = 'systemMusic'
let progressInterval: any = 0
let socket
const searchText = ref('')
const nowState: any = ref('stop') // 当前播放状态
const delayStatus = ref('system')
const durationStatus = ref('system')
const isPlay = ref(false)
const active = ref(false)
const placement = ref<DrawerPlacement>('left')
const selectMode = ref("order")
let cycleMusic: any = {}
let shortcutKeys = {} // 快捷键按键

const modeColumns = [
  {
    label: t('rule.order'),
    value: 'order'
  },
  {
    label: t('rule.random'),
    value: 'random'
  },
  {
    label: t('rule.cycle'),
    value: 'cycle'
  }
]

const musicColumns = [
  {
    title: t('columns.name'),
    key: 'name',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: t('columns.total_duration'),
    key: 'total_duration',
    width: 80,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    },
    sorter: (row1, row2) => timeToSeconds(row1.total_duration) - timeToSeconds(row2.total_duration)
  },
  {
    title: t('columns.operation'),
    key: 'operation',
    width: 60,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text: true,
          onClick: () => {
            heartClick(row.truthName, true)
            window.api.sync_sheet_2_el()
          }
        },
        {
          default: () => {
            return music.myFavorite.filter((res) => {
              return res.truthName.replaceAll('.mp3').includes(row.truthName)
            }).length == 0
              ? '❤'
              : null
          }
        }
      )
    }
  }
]

const favoritColumns = [
  {
    title: t('columns.name'),
    key: 'name',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: t('columns.total_duration'),
    key: 'total_duration',
    width: 80,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    },
    sorter: (row1, row2) => timeToSeconds(row1.total_duration) - timeToSeconds(row2.total_duration)
  },
  {
    title: t('columns.operation'),
    key: 'operation',
    width: 60,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text: true,
          onClick: () => {
            heartClick(row.truthName, false)
            window.api.sync_sheet_2_el()
          }
        },
        {
          default: () => {
            return '💔'
          }
        }
      )
    }
  }
]

const myImportColumns = [
  {
    title: t('columns.name'),
    key: 'name',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: t('columns.total_duration'),
    key: 'total_duration',
    width: 80,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    },
    sorter: (row1, row2) => timeToSeconds(row1.total_duration) - timeToSeconds(row2.total_duration)
  },
  {
    title: t('columns.operation'),
    key: 'operation',
    width: 60,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text: true,
          onClick: () => {
            deleteClick(row.truthName)
            window.api.sync_sheet_2_el()
          }
        },
        {
          default: () => {
            return '❌'
          }
        }
      )
    }
  }
]

const musicListColumns = [
  {
    title: t('columns.name'),
    key: 'name',
    resizable: true,
    className: 'th_css'
  }
]

function timeToSeconds(timeString) {
    var splitTime = timeString.split(':');

    // 如果是 HH:MM:SS 格式
    if (splitTime.length === 3) {
        var hours = parseInt(splitTime[0], 10);
        var minutes = parseInt(splitTime[1], 10);
        var seconds = parseInt(splitTime[2], 10);
        return hours * 3600 + minutes * 60 + seconds;
    }

    // 如果是 MM:SS 格式
    if (splitTime.length === 2) {
        var minutes = parseInt(splitTime[0], 10);
        var seconds = parseInt(splitTime[1], 10);
        return minutes * 60 + seconds;
    }

    return 0; // 如果格式不正确，返回0
}

const progress = ref(0.0) // 播放进度条
const nowTotalTime = ref<string>("00:00") // 播放总时间
const nowCurrentTime = ref<string>("00:00") // 播放时间
const playSpeed = ref(1) // 播放速度
const delaySpeed: any = ref(0) // 延迟设置
const durationSpeed: any = ref(0) // 延音设置
const durationRandomStart: any = ref(0.5)
const durationRandomEnd: any = ref(1.5)
const delayRandomStart: any = ref(0.01)
const delayRandomEnd: any = ref(0.06)
let clickTimeout: any = null

// ---------------------------------------------------
// 事件处理函数和工具函数
// ---------------------------------------------------

// 单击/双击选择音乐
const MusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      if (clickTimeout) {
        clearTimeout(clickTimeout);
        clickTimeout = null;
        playBarClickHandler("start", "")
      } else {
        nowSelectMusic.value = row.name;
        nowSelectMusicTruth = row.truthName;
        clickTimeout = setTimeout(() => {
          clickTimeout = null;
          store.commit('addPlayList', { 'name': row.name, 'truthName': row.truthName, 'type': nowType });
        }, 300);
      }
    }
  }
};

// 播放列表项点击（用于删除播放列表项）
const musicListSelect = (row: RowData, rowIndex: number) => {
  console.log(row)
  return {
    onClick: () => {
      store.commit("removePlayList", rowIndex)
      music.musicList = store.getters.getPlayList
    }
  }
};

// 刷新播放列表
function reloadMusicList() {
  active.value = !active.value;
  music.musicList = store.getters.getPlayList
}

// 开始进度条追踪
function startProgressTracking() {
  if (progressInterval) return;
  progressInterval = setInterval(getProgress, 1000);
}

// 停止进度条追踪
function stopProgressTracking() {
  if (progressInterval) {
    clearInterval(progressInterval);
    progressInterval = 0;
  }
}

// 清空播放列表
function clearPlayList() {
  store.commit('clearPlayList')
  music.musicList = store.getters.getPlayList
}

// 播放条点击处理函数
const playBarClickHandler = async (status: String, type: String) => {
  stopProgressTracking();
  if (status === 'resume') {
    if (nowState.value == 'stop') {
      message.info(t('messeage.double_click'));
      return;
    }
    sendData('play_operate', { "operate": "resume" });
    isPlay.value = true;
    startProgressTracking();
  }
  else if (status === 'pause') {
    sendData('play_operate', { "operate": "pause" });
    isPlay.value = false;
    stopProgressTracking();
  }
  else if (status === 'stop') {
    sendData('play_operate', { "operate": "stop" });
    await clearPlayInfo();
  }
  else if (status === 'start') {
    setTimeout(() => {
      sendData('play_operate', {
        fileName: nowSelectMusicTruth,
        type: type != "" ? type : nowType,
        operate: "start"
      }).then(() => {
        progress.value = 0;
        nowTotalTime.value = '00:00';
        nowCurrentTime.value = '00:00';
        cycleMusic = {
          fileName: nowSelectMusicTruth,
          type: type != "" ? type : nowType,
        };
      });
      message.success('开始');
      isPlay.value = true;
      startProgressTracking();
    });
  }
  else if (status === 'next') {
    // 直接调用下一首逻辑，不依赖 progress.value = 100 触发
    if (selectMode.value === 'order') {
      orderMusicPlay();
    } else if (selectMode.value === 'random') {
      randomMusicPlay();
    } else if (selectMode.value === 'cycle') {
      cycleMusicPlay();
    }
    return;
  }
  nowState.value = status;
};

// 拖动进度条开始（暂停播放）
function drag_progress_start() {
  sendData('play_operate',{"operate":"pause"}).then(() => {
    clearInterval(progressInterval)
  })
}

// 拖动进度条结束（恢复播放）
function drag_progress_end() {
  clearInterval(progressInterval);
  setConfig('set_progress', progress.value / 100)
  sendData('play_operate',{"operate":"resume"}).then(() => {
    progressInterval = setInterval(getProgress, 1000)
  })
}

// 获取播放进度
async function getProgress() {
  try {
    // 如果当前状态为暂停或停止，则不更新进度
    if (nowState.value === 'pause' || nowState.value === 'stop') {
      return "paused_or_stopped";
    }
    // 当进度达到或超过 100 时，认为本曲播放完毕
    if (progress.value >= 100) {
      // 停止定时器，防止重复调用
      stopProgressTracking();
      clearPlayInfo();
      // 根据不同播放模式，延时调度下一曲
      if (selectMode.value === 'order') {
        setTimeout(orderMusicPlay, 500);
      } else if (selectMode.value === 'random') {
        setTimeout(randomMusicPlay, 500);
      } else if (selectMode.value === 'cycle') {
        setTimeout(cycleMusicPlay, 500);
      }
    } else {
      // 请求最新进度数据
      const res = await getData('getProgress');
      if (res && res.now_progress !== undefined) {
        // 更新进度，转换为数字
        progress.value = Number(res.now_progress);
        nowPlayMusic.value = res.now_play_music || t('messeage.unknow_music');
        nowTotalTime.value = res.now_total_time;
        nowCurrentTime.value = res.now_current_time;
      }
    }
  } catch (error) {
    console.error('getProgress 出错：', error);
  }
  return "ok";
}

// 随机播放
function randomMusicPlay() {
  nowSelectMusicTruth = music.systemMusic[Math.floor(Math.random() * (music.systemMusic.length))].truthName
  playBarClickHandler("start", 'systemMusic')
}

// 顺序播放
async function orderMusicPlay() {
  let struct = store.getters.getNextPlayMusic
  if (struct != null && struct != undefined) {
    nowSelectMusicTruth = struct.truthName
    let type = struct.type
    playBarClickHandler("start", type)
  } else {
    clearInterval(progressInterval)
    playBarClickHandler("stop","")
    console.log("叽里呱啦")
    setTimeout(()=>{window.api.system_notification("😳", t('messeage.order_ok'))},1000)
    nowPlayMusic.value = t('messeage.no_music')
  }
}

// 循环播放
function cycleMusicPlay() {
  nowSelectMusicTruth = cycleMusic?.fileName
  playBarClickHandler("start", cycleMusic?.type)
}

// 更新数据（如收藏、系统音乐、导入音乐、扒谱音乐）
function handleUpdateValue(value: string) {
  tabsNumber.value = value
  getListData(value)
}

// 处理抽屉切换前动作
function handleBeforeLeave(name: string) {
  nowType = name
  return true
}

// 清除播放信息（停止定时器、重置状态）
function clearPlayInfo() {
  // 先清除轮询定时器
  stopProgressTracking();
  nowSelectMusic.value = t('controller.no_music');
  nowPlayMusic.value = t('messeage.no_music');
  nowState.value = 'stop';
  progress.value = 0;
  nowTotalTime.value = '00:00';
  nowCurrentTime.value = '00:00';
  // 确保其他状态同步更新（如 statusbar，确保 statusbar 在当前上下文中有效）
  statusbar[0] = true;
  statusbar[1] = false;
  isPlay.value = false;
}

// 收藏点击处理
function heartClick(name, state) {
  if (state) {
    sendData('config_operate', {
      fileName: name,
      type: nowType,
      operate: 'favorite_music'
    }).then(() => {
      handleUpdateValue('myFavorite')
      handleUpdateValue(nowType)
      message.success(t('tab.love_success'))
    })
  } else {
    sendData('config_operate', {
      fileName: name,
      type: 'myFavorite',
      operate: "drop_file"
    }).then(() => {
      handleUpdateValue('myFavorite')
      message.success(t('tab.remove_success'))
    })
  }
}

// 删除点击处理
function deleteClick(name) {
  sendData('config_operate', {
    fileName: name,
    type: 'myImport',
    operate: "drop_file"
  }).then(() => {
    handleUpdateValue('myImport')
    message.success(t('tab.remove_success'))
  })
}

// 文件上传完成后的处理
function handleFinish({ file: _file, event: _event }) {
  handleUpdateValue('myImport')
  nowType = "myImport"
  window.api.sync_sheet_2_el()
}

// 文件上传前处理
function beforeFileUpload(file) {
  return window.api.readFile(file.file.file.path, false).then(res => {
    if (res) {
      message.success(t('messeage.sheet') + file.file.file.name + t('messeage.ok_import') )
    } else {
      message.error(t('messeage.sheet') + file.file.file.name + t('messeage.no_import') )
    }
    return res;
  })
}

// 获取列表数据
async function getListData(value) {
  await getList(value, searchText.value).then((_res) => {
    console.log('list11',_res);
    eval('music.' + value + '=_res')
  })
}

// ---------------------------------------------------
// 监听器（watch）
// ---------------------------------------------------
const fetchListData = debounce(() => {
  getListData('myFavorite');
  getListData('systemMusic');
  getListData('myImport');
  getListData('myTranslate');
}, 200);
watch(searchText, fetchListData)

let isConfigDelayStatus = false
let randomInterval: any = null
watch(delayStatus, () => {
  if (isConfigDelayStatus) {
    isConfigDelayStatus = false
    return
  }
  configStore.setItem(CONFIG_TYPE.DELAY_STATUS, delayStatus.value)
  switch (delayStatus.value) {
    case 'system':
      delaySpeed.value = 0
      clearInterval(randomInterval)
      break
    case 'random':
      delayRandomStart.value = 0.01
      delayRandomEnd.value = 0.06
      randomInterval = setInterval(() => {
        delaySpeed.value = (Math.random() * (delayRandomEnd.value - delayRandomStart.value) + delayRandomStart.value).toFixed(3)
      }, 1000)
      break
    case 'custom':
      delaySpeed.value = 0
      clearInterval(randomInterval)
      break
  }
})
watch(delayRandomStart, ()=>{
  configStore.setItem(CONFIG_TYPE.DELAY_RANDOM_START, delayRandomStart.value)
})
watch(delayRandomEnd, ()=>{
  configStore.setItem(CONFIG_TYPE.DELAY_RANDOM_END, delayRandomEnd.value)
})

let isConfigDurationStatus = false
let durationInterval: any = null
watch(durationStatus, () => {
  if (isConfigDurationStatus) {
    isConfigDurationStatus = false
    return
  }
  configStore.setItem(CONFIG_TYPE.DURATION_STATUS, durationStatus.value)
  switch (durationStatus.value) {
    case 'system':
      durationSpeed.value = 0
      clearInterval(durationInterval)
      break
    case 'random':
      durationRandomStart.value = 0.01
      durationRandomEnd.value = 1.5
      durationInterval = setInterval(() => {
        durationSpeed.value = (Math.random() * (durationRandomEnd.value - durationRandomStart.value) + durationRandomStart.value).toFixed(3)
      }, 1000)
      break
    case 'custom':
      durationSpeed.value = 0
      clearInterval(durationInterval)
      break
  }
})
watch(durationRandomStart, ()=>{
  configStore.setItem(CONFIG_TYPE.DURATION_RANDOM_START, durationRandomStart.value)
})
watch(durationRandomEnd, ()=>{
  configStore.setItem(CONFIG_TYPE.DURATION_RANDOM_END, durationRandomEnd.value)
})

watch(delaySpeed, () => {
  if(delayStatus.value !== CONFIG_STATUS_TYPE.RANDOM){
    configStore.setItem(CONFIG_TYPE.DELAY_SPEED, delaySpeed.value)
  }
  setConfig('delay_interval', delaySpeed.value)
})
watch(durationSpeed, () => {
  if(durationSpeed.value !== CONFIG_STATUS_TYPE.RANDOM){
    configStore.setItem(CONFIG_TYPE.DURATION_SPEED, durationSpeed.value)
  }
  console.log('延音设置11durationSpeed',durationSpeed.value);
  setConfig('duration', durationSpeed.value)
})
watch(playSpeed, () => {
  configStore.setItem(CONFIG_TYPE.PLAY_SPEED, playSpeed.value)
  setConfig('play_speed', playSpeed.value)
})

const systemMusic = ref<DataTableInst>()
const myImport = ref<DataTableInst>()
const myTranslate = ref<DataTableInst>()
const myFavorite  = ref<DataTableInst>()
const tabsNumber = ref("systemMusic")
function locationNowPlayMusic(){
  searchText.value = ""
  Promise.all([getListData('myFavorite'), getListData('systemMusic'), getListData('myImport'), getListData('myTranslate')]).then(function(){
    let index = eval("music." + tabsNumber.value + ".findIndex(item => item.name === nowPlayMusic.value)")
    if (index === -1){
      message.error(t('messeage.no_now') )
      return
    }
    eval(`music.${tabsNumber.value}[${index}].position = true`)
    eval(`${tabsNumber.value}.value?.scrollTo({index, behavior: 'smooth',})`)
    setTimeout(() => {
      eval(`music.${tabsNumber.value}[${index}].position = false`)
    }, 5000);
  });
}
function rowClassName(row: RowData) {
  if (row?.position) {
    return 'table_position'
  }
  return 'td_css'
}

// ---------------------------------------------------
// WebSocket 初始化及相关处理
// ---------------------------------------------------
function initWebSocket() {
  socket = new WebSocket('ws://127.0.0.1:11452')
  // 添加 WebSocket 事件监听
  socket.onopen = () => {
    console.log('WebSocket 已连接')
  }
  socket.onmessage = (event) => {
    const key = decodeURIComponent(event.data).trim() // 获取按下的按键
    console.log("按下",key)
    if (key === shortcutKeys["start"]) {
      if (nowState.value != 'stop') {
        window.api.system_notification("🍎", t('messeage.msg1'))
      } else {
        console.log("else")
        if (nowSelectMusic.value === t('controller.no_music')) {
          window.api.system_notification("😭", t('messeage.msg2'))
        } else {
          window.api.system_notification("✔", t('messeage.msg3'))
          playBarClickHandler('start', '')
        }
      }
    }
    if (key === shortcutKeys["resume"]) {
      if (nowState.value === 'pause') {
        window.api.system_notification("▶", t('messeage.msg4'))
        playBarClickHandler('resume', '')
      } else {
        window.api.system_notification("🍎", t('messeage.msg5'))
      }
    }
    if (key === shortcutKeys["pause"]) {
      if (isPlay.value) {
        window.api.system_notification("⏸", t('messeage.msg6'))
        playBarClickHandler('pause', '')
      } else {
        window.api.system_notification("🍎", t('messeage.msg7'))
      }
    }
    if (key === shortcutKeys["stop"]) {
      window.api.system_notification("🛑", t('messeage.msg8'))
      playBarClickHandler('stop', '')
    }
    if (key === shortcutKeys["next"]) {
      window.api.system_notification("⏩", t('messeage.msg9'))
      playBarClickHandler('next', '')
    }
    if (key === shortcutKeys["add_duration"]) {
  if (durationSpeed.value * 100 === 200) {
    message.info(t('messeage.msg10'));
  } else {
    durationStatus.value = "custom";
    setTimeout(()=>{
      durationSpeed.value = Math.round((durationSpeed.value + 0.01) * 100) / 100;
    })
    message.info(t('messeage.msg11'));
  }
}
if (key === shortcutKeys["reduce_duration"]) {
  if (durationSpeed.value * 100 === 0) {
    message.info(t('messeage.msg12'));
  } else {
    setTimeout(()=>{
      durationStatus.value = "custom";
      durationSpeed.value = Math.round((durationSpeed.value - 0.01) * 100) / 100;
    })
    message.info(t('messeage.msg13'));
  }
}
if (key === shortcutKeys["add_delay"]) {
  if (delaySpeed.value * 100 === 200) {
    message.info(t('messeage.msg14'));
  } else {
    delayStatus.value = "custom";
    setTimeout(()=>{
      delaySpeed.value = Math.round((delaySpeed.value + 0.01) * 100) / 100;
    })
    message.info(t('messeage.msg15'));
  }
}
if (key === shortcutKeys["reduce_delay"]) {
  if (delaySpeed.value * 100 === 0) {
    message.info(t('messeage.msg16'));
  } else {
    delayStatus.value = "custom";
    setTimeout(()=>{
      delaySpeed.value = Math.round((delaySpeed.value - 0.01) * 100) / 100;
    })
    message.info(t('messeage.msg17'));
  }
}
if (key === shortcutKeys["add_speed"]) {
  if (playSpeed.value * 10 === 50) {
    message.info(t('messeage.msg18'));
  } else {
    message.info(t('messeage.msg19'));
    playSpeed.value = Math.round((playSpeed.value + 0.1) * 10) / 10;
  }
}
if (key === shortcutKeys["reduce_speed"]) {
  if (playSpeed.value * 10 === 1) {
    message.info(t('messeage.msg20'));
  } else {
    playSpeed.value = Math.round((playSpeed.value - 0.1) * 10) / 10;
    message.info(t('messeage.msg21'));
  }
}
  }
  socket.onclose = () => {
    console.log('WebSocket 已断开')
  }
  socket.onerror = (error) => {
    console.error('WebSocket 出现错误', error)
  }
}

sendData("config_operate",{
    "operate": "get",
    "name": "shortcutStruct"
}).then(res=>{
  shortcutKeys = res["music_key"]
  console.log(shortcutKeys)
})
initWebSocket()


const getConfigStore = () => {
  // 处理延迟状态配置
  const savedDelayStatus = configStore.getItem(CONFIG_TYPE.DELAY_STATUS)
  if (savedDelayStatus) {
    isConfigDelayStatus = true
    delayStatus.value = savedDelayStatus
    if (savedDelayStatus === 'random') {
      delayRandomStart.value = configStore.getItem(CONFIG_TYPE.DELAY_RANDOM_START) || 0.01
      delayRandomEnd.value = configStore.getItem(CONFIG_TYPE.DELAY_RANDOM_END) || 0.06
      clearInterval(randomInterval)
      randomInterval = setInterval(() => {
        delaySpeed.value = (Math.random() * (delayRandomEnd.value - delayRandomStart.value) + delayRandomStart.value).toFixed(3)
      }, 1000)
    } else if (savedDelayStatus === 'custom') {
      delaySpeed.value = configStore.getItem(CONFIG_TYPE.DELAY_SPEED) || 0
      clearInterval(randomInterval)
    } else {
      delaySpeed.value = 0
      clearInterval(randomInterval)
    }
  }

  // 处理延音状态配置
  const savedDurationStatus = configStore.getItem(CONFIG_TYPE.DURATION_STATUS)
  if (savedDurationStatus) {
    isConfigDurationStatus = true
    durationStatus.value = savedDurationStatus
    if (savedDurationStatus === 'random') {
      durationRandomStart.value = configStore.getItem(CONFIG_TYPE.DURATION_RANDOM_START) || 0.5
      durationRandomEnd.value = configStore.getItem(CONFIG_TYPE.DURATION_RANDOM_END) || 1.5
      clearInterval(durationInterval)
      durationInterval = setInterval(() => {
        durationSpeed.value = (Math.random() * (durationRandomEnd.value - durationRandomStart.value) + durationRandomStart.value).toFixed(3)
      }, 1000)
    } else if (savedDurationStatus === 'custom') {
      durationSpeed.value = configStore.getItem(CONFIG_TYPE.DURATION_SPEED) || 0
      clearInterval(durationInterval)
    } else {
      durationSpeed.value = 0
      clearInterval(durationInterval)
    }
  }
  // 设置播放速度
  configStore.getItem(CONFIG_TYPE.PLAY_SPEED) && (playSpeed.value = configStore.getItem(CONFIG_TYPE.PLAY_SPEED))
  if (configStore.getItem(CONFIG_TYPE.DURATION_SPEED) == 0 || configStore.getItem(CONFIG_TYPE.DURATION_SPEED) == undefined){
      durationStatus.value = 'custom'
      durationSpeed.value = 0.03
      console.log("拨正")
  }
}

onMounted(async ()=>{
  await handleUpdateValue('myFavorite')
  await handleUpdateValue('systemMusic')
  getConfigStore()
})

// ---------------------------------------------------
// 组件销毁时的清理工作
// ---------------------------------------------------
onUnmounted(async () => {
  if (socket) {
    socket.close()
    socket = null
  }
  playBarClickHandler("stop", "")
  setConfig('delay_interval', 0)
  setConfig('duration', 0)
  setConfig('play_speed', 1)
  clearPlayInfo()
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
  --n-caret-color: rgb(242,232,196)!important;
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

:deep(.table_position td) {
  background-color: rgba(242, 201, 196, 0.507) !important;
}

.actionButton{
  margin-left: 20px;
}
</style>
