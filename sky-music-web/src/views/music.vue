<template>
  <n-flex align="center">
    <n-gradient-text :size="24" type="success" style="width: 100%">
      {{ "当前: " + nowPlayMusic + "" }}
    </n-gradient-text>
    <n-space vertical> </n-space>
    <n-progress
      style="max-width: 50%"
      type="line"
      :percentage="progress"
      indicator-placement="inside"
      processing
    />
    <n-radio-group
      v-model:value="nowState"
      name="radiobuttongroup1"
      @update:value="playSelect"
    >
      <n-radio-button
        v-for="status in statusColumns"
        :key="status.value"
        :value="status.value"
        :label="status.label"
      />
    </n-radio-group>

    <n-gradient-text :size="20" type="success" style="width: 110px">
      {{ "状态: " + nowState }}
    </n-gradient-text>
    <n-space vertical>
      延迟设置
      <n-slider v-model:value="delaySpeed" range :step="1" />
      <n-space>
        <n-input-number v-model:value="delaySpeed[0]" size="small" />
        <n-input-number v-model:value="delaySpeed[1]" size="small" />
      </n-space>
    </n-space>
  </n-flex>

  <n-card style="margin-top: 20px">
    <n-tabs type="line" animated>
      <n-tab-pane name="musicData" tab="自带歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.musicData"
          :bordered="false"
          :max-height="330"
          virtual-scroll
          :row-props="systemMusicSelect"
        />
      </n-tab-pane>
      <n-tab-pane name="importMusic" tab="导入的歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.importData"
          :bordered="false"
          :max-height="300"
          :scroll-x="1800"
          virtual-scroll
          :row-props="myImportMusicSelect"
        />
      </n-tab-pane>
      <n-tab-pane name="transforMusic" tab="转换的歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.translateData"
          :bordered="false"
          :max-height="250"
          :scroll-x="1800"
          virtual-scroll
          :row-props="myTranslateMusicSelect"
        />
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>

<script lang="ts" setup>
import { getData, sendData } from "@/utils/fetchUtils";
import { RowData } from "naive-ui/es/data-table/src/interface";
import { reactive, ref, watch } from "vue";
import { useMessage } from 'naive-ui'
const message = useMessage()


let music: any = reactive({
  // 音乐列表
  musicData: [], // 原版音乐
  importData: [], // 导入的音乐
  translateData: [], // 扒谱的音乐
});
let nowPlayMusic = ref("没有歌曲"); // 当前选中歌曲
let nowType = ""
let nowState = ref("stop"); // 当前播放状态
let statusColumns = [
  {
    value: "start",
    label: "开始",
  },
  {
    value: "resume",
    label: "继续",
  },
  {
    value: "pause",
    label: "暂停",
  },
  {
    value: "stop",
    label: "停止",
  },
]; // 播放按钮
let musicColumns = [
  {
    title: "歌名",
    key: "name",
  },
]; // 音乐列

let progress = ref(0.0); // 播放进度条
let playSpeed = ref(1); // 播放速度
let delaySpeed = ref([50, 70]); // 延迟设置

const systemMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
      nowType = "systemMusic"
    },
  };
};
const myImportMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
      nowType = "myImport"
    },
  };
};
const myTranslateMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
      nowType = "myTranslate"
    },
  };
};

let progressInterval = 0

const playSelect = (value: string) => {
  console.log(value)
  switch (value) {
    case "start":
      sendData("start",{
        fileName:nowPlayMusic.value,
        type:nowType
      });
      message.success("开始")
      progressInterval = setInterval(getProgress,1000)
      break;
    case "pause":
      getData("pause");
      clearInterval(progressInterval)

      break;
    case "stop":
      getData("stop");
      message.error("中止")
      clearInterval(progressInterval)
      break;
    case "resume":
      getData("resume")
      progressInterval = setInterval(getProgress,1000)
  }
};

function getProgress(){
  getData("getProgress").then(res => {
    progress.value = res
  });
}

getData("").then((res: { systemMusic: any; myImport: any; myTranslate: any }) => {
  music.musicData.push(...res.systemMusic);
  music.importData.push(...res.myImport);
  music.translateData.push(...res.myTranslate);
});
</script>
