<template>
  <n-flex align="center">
    <n-gradient-text :size="20" type="success" style="width: 100%">
      {{ "当前播放: " + nowPlayMusic + "" }}
      <br>
      <n-progress style="max-width: 60%; display: inline-block" type="line" :percentage="progress"
        indicator-placement="inside" processing :color="{ stops: ['white', 'blue'] }" @click="progressClick" />
    </n-gradient-text>
    <n-radio-group v-model:value="nowState" name="radiobuttongroup1" @update:value="playSelect">
      <n-radio-button v-for="status in statusColumns" :key="status.value+status.show" :value="status.value" :label="status.label"
        v-show="status.show" :disabled="status.disabled" />
    </n-radio-group>
    <n-upload action="http://localhost:9899/userMusicUpload" multiple style="width: 100px; height: 34px" accept=".txt"
      :show-file-list="false" @finish="handleFinish">
      <n-button type="info" ghost>
        上传我的文件
      </n-button>
    </n-upload>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13">
          间隔延迟s&nbsp;&nbsp;&nbsp;
        </n-gradient-text>
        <n-radio-group v-model:value="delayStatus" name="radiogroup" @update:value="delaySelect">
          <n-space>
            <n-radio key="system" value="system">系统自带</n-radio>
            <n-radio key="random" value="random">随机</n-radio>
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col :span="9" style="margin-left: -50px;" v-show="delayStatus == 'custom'">
        <n-space vertical style="width: 150px; float: right; margin-top: 2px;">
          <n-slider v-model:value="delaySpeed" :step="0.1" :min="0.01" :max="2" />
        </n-space>
      </n-col>
    </n-row>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13">
          延音设置s&nbsp;&nbsp;&nbsp;
        </n-gradient-text>
        <n-radio-group v-model:value="sustainStatus" name="radiogroup" @update:value="delaySelect">
          <n-space>
            <n-radio key="system" value="system">系统自带</n-radio>
            <n-radio key="random" value="random">随机</n-radio>
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col :span="9" style="margin-left: -50px;" v-show="sustainStatus == 'custom'">
        <n-space vertical style="width: 150px; float: right; margin-top: 2px;">
          <n-slider v-model:value="sustainSpeed" :step="0.1" :min="0.02" :max="1.5" />
        </n-space>
      </n-col>
    </n-row>
    <n-row gutter="12">
      <n-col :span="15">
        <n-gradient-text type="info" :size="13">
          播放延迟s&nbsp;&nbsp;&nbsp;
        </n-gradient-text>
        <n-radio-group v-model:value="playDelayStatus" name="radiogroup" @update:value="delaySelect">
          <n-space>
            <n-radio key="system" value="system">无</n-radio>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <n-radio key="custom" value="custom">自定义</n-radio>
          </n-space>
        </n-radio-group>
      </n-col>
      <n-col :span="9" style="margin-left: -50px;" v-show="playDelayStatus == 'custom'">
        <n-space vertical style="width: 150px; float: right; margin-top: 2px;">
          <n-slider v-model:value="playDelay" :step="1" :min="1" :max="10" />
        </n-space>
      </n-col>
    </n-row>
  </n-flex>

  <n-card style="margin-top: 20px">
    <n-tabs type="bar" animated @update:value="handleUpdateValue" @before-leave="handleBeforeLeave" size="small">
      <n-tab-pane name="systemMusic" tab="自带歌曲">
        <n-data-table :columns="musicColumns" :data="music.systemMusic" :bordered="false" :max-height="301"
          virtual-scroll :min-row-height="18" :scroll-x="100" :row-props="systemMusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myImport" tab="导入歌曲">
        <n-data-table :columns="musicColumns" :data="music.myImport" :bordered="false" :max-height="300"
          :min-row-height="18" :row-props="myImportMusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="转换歌曲">
        <n-data-table :columns="musicColumns" :data="music.myTranslate" :bordered="false" :max-height="250"
          :row-props="myTranslateMusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myFavorite" tab="收藏">
        <n-data-table :columns="favoritColumns" :data="music.myFavorite" :bordered="false" :max-height="250"
          :row-props="myFavoriteMusicSelect" />
      </n-tab-pane>
      <template #suffix>
        <n-input round placeholder="搜索" v-model:value="searchText"
          style="margin-bottom: 5px; width: 25vh; margin-left: 5px;">
          <template #suffix>
            <n-icon :component="Search" />
          </template>
        </n-input>
      </template>
    </n-tabs>
  </n-card>
</template>

<script lang="ts" setup>
import { getData, sendData, getList, setConfig } from "@/utils/fetchUtils";
import { RowData } from "naive-ui/es/data-table/src/interface";
import { h, reactive, ref, watch } from "vue";
import { NButton, useMessage } from 'naive-ui'
import { Search } from '@vicons/ionicons5'
const message = useMessage()


let music: any = reactive({
  // 音乐列表
  systemMusic: [], // 原版音乐
  myImport: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
  myFavorite: [] // 我的最爱
});
let nowPlayMusic = ref("没有歌曲"); // 当前选中歌曲
let nowType = "systemMusic"
let searchText = ref("")
let nowState = ref("stop"); // 当前播放状态
let delayStatus = ref("system")
let sustainStatus = ref("system")
let playDelayStatus = ref("system")
let statusColumns = [
  {
    value: "start",
    label: "开始",
    show: true,
    disabled:false
  },
  {
    value: "resume",
    label: "继续",
    show: false,
    disabled:false
  },
  {
    value: "pause",
    label: "暂停",
    show: false,
    disabled:false
  },
  {
    value: "stop",
    label: "停止",
    show: true,
    disabled:false
  },
]; // 播放按钮
let musicColumns = [
  {
    title: "歌名",
    key: "name",
    resizable: true,
  }, {
    title: '操作',
    key: 'operation',
    width: 100,
    render(row) {
      return h(
        NButton,
        {
          size: 'medium',
          text: music.myFavorite.filter(res => { return res.name.replaceAll(".mp3").includes(row.name) }).length == 0 ? false : true,
          onClick: () => heartClick(row.name, true)
        },
        {
          default: () => {
            return music.myFavorite.filter(res => { return res.name.replaceAll(".mp3").includes(row.name) }).length == 0 ?
              "❤" : null
          }
        }
      )
    }
  }
]; // 音乐列

let favoritColumns = [
  {
    title: "歌名",
    key: "name",
    resizable: true,
  }, {
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
]; // 音乐列

let progress = ref(0.0); // 播放进度条
let playSpeed = ref(1); // 播放速度
let delaySpeed = ref(0.01); // 延迟设置
let sustainSpeed = ref(0.02); // 延音设置
let playDelay = ref(0) // 播放延迟

const systemMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
    },
  };
};
const myImportMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
    },
  };
};
const myTranslateMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
    },
  };
};
const myFavoriteMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
    },
  };
};

let progressInterval: any = 0

const playSelect = (value: string) => {
  console.log("value",value)
  switch (value) {
    case "start":
      if (nowPlayMusic.value === "没有歌曲") {
        message.error("选个歌再播放吧靓仔")
        nowState.value = 'stop'
        return;
      }
      setTimeout(() => {
        sendData("start", {
          fileName: nowPlayMusic.value,
          type: nowType
        });
        message.success("开始")
        progressInterval = setInterval(getProgress, 1000)
      }, playDelay.value * 1000)
      statusColumns[0].show = false;
      statusColumns[1].show = true;
      statusColumns[2].show = true;
      statusColumns[3].show = true;
      statusColumns[0].disabled = true;
      statusColumns[1].disabled = true;
      statusColumns[2].disabled = false;
      statusColumns[3].disabled = false;
      break;
    case "resume":
      getData("resume")
      progressInterval = setInterval(getProgress, 1000)
      statusColumns[0].disabled = true;
      statusColumns[1].disabled = false;
      statusColumns[2].disabled = false;
      statusColumns[3].disabled = false;
      break;
    case "pause":
      getData("pause");
      clearInterval(progressInterval)
      progressInterval = 0
      statusColumns[0].disabled = false;
      statusColumns[1].disabled = false;
      statusColumns[2].disabled = false;
      statusColumns[3].disabled = false;
      break;
    case "stop":
      getData("stop");
      clearPlayInfo()
      statusColumns[0].disabled = false;
      statusColumns[1].disabled = false;
      statusColumns[2].disabled = false;
      statusColumns[3].disabled = false;
      break;
  }
};

const delaySelect = (value: string) => {
  switch (value) {
    case "system":
      break;
    case "random":
      break;
  }
};

function progressClick(event) {
  if (nowState.value === 'stop') {
    message.error("没有歌曲在播放，请播放歌曲后继续操作")
    return
  }
  // 获取点击事件对象
  const rect = event.currentTarget.getBoundingClientRect(); // 获取组件的边界框
  const clickPosition = event.clientX - rect.left; // 计算点击位置（相对于组件左边）
  const componentWidth = rect.width; // 获取组件的总宽度
  // 计算百分比
  const percentage = (clickPosition / componentWidth) * 100;
  // 更新进度条
  progress.value = parseFloat(Math.min(Math.max(percentage, 0), 100).toFixed(1)) // 限制在0-100之间
  setConfig("set_progress", progress.value / 100)
}

function getProgress() {
  getData("getProgress").then(res => {
    progress.value = res.now_progress
  });
}


handleUpdateValue("myFavorite")
handleUpdateValue("systemMusic")

function handleUpdateValue(value: string) {
  searchText.value = ""
  getList(value).then(res => {
    eval("music." + value + "=res")
  })
}

function handleBeforeLeave(name: string){
  nowType = name
  return true;
}

watch(searchText, () => {
  if (searchText.value === "" || searchText.value === undefined || searchText.value === null) {
    handleUpdateValue("myFavorite")
    handleUpdateValue("systemMusic")
    handleUpdateValue("myImport")
    handleUpdateValue("myTranslate")
    return
  }
  music.systemMusic = music.systemMusic.filter((res) => { return res.name.includes(searchText.value) })
  music.myImport = music.myImport.filter((res) => { return res.name.includes(searchText.value) })
  music.myTranslate = music.myTranslate.filter((res) => { return res.name.includes(searchText.value) })
  music.myFavorite = music.myFavorite.filter((res) => { return res.name.includes(searchText.value) })
})

let randomInterval: any = null
watch(delayStatus, () => {
  switch (delayStatus.value) {
    case "system":
      setConfig("delay_interval", 0.01)
      clearInterval(randomInterval)
      break;
    case "random":
      randomInterval = setInterval(() => {
        setConfig("delay_interval", (Math.random() * (0.06 - 0.01) + 0.01).toFixed(3))
      }, 1000)
      break
    case "custom":
      setConfig("delay_interval", delaySpeed.value)
      clearInterval(randomInterval)
      break
  }
})

let sustainInterval: any = null
watch(sustainStatus, () => {
  switch (sustainStatus.value) {
    case "system":
      setConfig("sustain_time", 0.02)
      clearInterval(sustainInterval)
      break;
    case "random":
      sustainInterval = setInterval(() => {
        setConfig("sustain_time", (Math.random() * (0.6 - 0.02) + 0.02).toFixed(3))
      }, 1000)
      break
    case "custom":
      setConfig("sustain_time", sustainSpeed.value)
      clearInterval(sustainInterval)
      break
  }
})

watch(playDelayStatus, () => {
  if (playDelayStatus.value == 'system') {
    playDelay.value = 0
  }
})

watch(delaySpeed, () => {
  setConfig("delay_interval", delaySpeed.value)
})
watch(sustainSpeed, () => {
  setConfig("sustain_time", sustainSpeed.value)
})

function clearPlayInfo() {
  nowPlayMusic.value = "没有歌曲"
  nowState.value = "stop"
  progress.value = 0
  clearInterval(progressInterval)
  statusColumns[0].show = true;
  statusColumns[1].show = false;
  statusColumns[2].show = false;
  statusColumns[3].show = true;
}

//  收藏点击
function heartClick(name, state) {
  if (state) {
    sendData("setFavoriteMusic", {
      fileName: name,
      type: nowType
    }).then(() => {
      handleUpdateValue("myFavorite")
      handleUpdateValue("systemMusic")
      handleUpdateValue("myImport")
      handleUpdateValue("myTranslate")
      message.success("收藏成功")
    })
  } else {
    sendData("dropFile", {
      fileName: name,
      type: "myFavorite"
    }).then(() => {
      handleUpdateValue("myFavorite")
      handleUpdateValue("systemMusic")
      handleUpdateValue("myImport")
      handleUpdateValue("myTranslate")
      message.success("移除成功")
    })
  }

}

function handleFinish({ file, event }) {
  handleUpdateValue("myImport")
  message.success("OK~")
}
</script>
