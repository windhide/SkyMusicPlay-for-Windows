<template>
  <n-flex align="center">
    <n-gradient-text :size="24" type="success" style="width: 100%; color:#F2E8C4">
      转换歌曲
    </n-gradient-text>
    <n-upload
      action="http://localhost:9899/fileUpload"
      multiple
      style="width: 100px; height: 34px"
      accept=".mp3,.mp4,.flac,.mid"
      :show-file-list="false"
      @finish="handleFinish"
    >
    <n-button type="info" ghost  color="#F2C9C4"> step1.选择音乐 </n-button>
    </n-upload>
    <n-button type="primary" ghost :loading="processFlag" @click="handleStartTranslate" style="margin-left: 25px;" color="#F2E8C4">
      step2.开始转换
    </n-button>
    <n-divider style="margin:0px"/>
    <n-gradient-text type="info" :size="18" style="color: #F2C9C4">
      当前任务
      {{
        now_translate_text.process == undefined && now_translate_text.text == undefined
          ? "已完成"
          : now_translate_text.process + " " + now_translate_text.text
      }}
    </n-gradient-text>
    <div style="width: 100%">
      <n-gradient-text type="info" style="color: #F2C9C4"> 总体进度 </n-gradient-text>
      <n-progress
        color="#F2C9C4"
        style="max-width: 50%"
        type="line"
        :percentage="progress.overall_progress"
        indicator-placement="inside"
        processing
      />
    </div>
    <div style="width: 100%">
      <n-gradient-text type="info" style="color: #F2E8C4"> 当前歌曲MID转换 </n-gradient-text>
      <n-progress
        color="#F2E8C4"
        style="max-width: 50%"
        type="line"
        :percentage="progress.tran_mid_progress"
        indicator-placement="inside"
        processing
      />
    </div>
  </n-flex>

  <n-card style="margin-top: 20px">
    <n-tabs type="line" animated @update:value="handleUpdateValue">
      <n-tab-pane name="translateOriginalMusic" tab="未转换歌曲">
        <n-data-table
          :columns="originalColumns"
          :data="music.translateOriginalMusic"
          :bordered="false"
          :max-height="330"
          :scroll-x="100"
          row-class-name="td_css"
        />
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="已转换歌曲">
        <n-data-table
          :columns="translateColumns"
          :data="music.myTranslate"
          :bordered="false"
          :max-height="300"
          :scroll-x="100"
          row-class-name="td_css"
        />
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>

<script lang="ts" setup>
import { getData, sendData, getList } from "@renderer/utils/fetchUtils";
import { h, reactive, ref, watch } from "vue";
import { NButton, useMessage } from "naive-ui";
const message = useMessage();
const processFlag = ref(false);

const music: any = reactive({
  // 音乐列表
  translateOriginalMusic: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
});
const progress: any = reactive({
  translate_progress: 0,
  overall_progress: 0,
  tran_mid_progress: 0,
});
const now_translate_text = reactive({
  process: "",
  text: "",
});

const originalColumns = [
  {
    title: "歌名",
    key: "name",
    className: 'th_css'
  },
  {
    title: "操作",
    key: "operation",
    width: 100,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: "medium",
          text: false,
          onClick: () => originalClick(row.name),
        },
        {
          default: () => {
            return "❌";
          },
        }
      );
    },
  },
]; // 音乐列

const translateColumns = [
  {
    title: "歌名",
    key: "name",
    className: 'th_css'
  },
  {
    title: "操作",
    key: "operation",
    width: 100,
    className: 'th_css',
    render(row) {
      return h(
        NButton,
        {
          size: "medium",
          text: false,
          onClick: () => translateClick(row.name),
        },
        {
          default: () => {
            return "❌";
          },
        }
      );
    },
  },
]; // 音乐列

function originalClick(name) {
    sendData("config_operate", {
      fileName: name.slice(0, name.lastIndexOf('.')),
      type: 'translateOriginalMusic',
      suffix: name.match(/(\.[^.]*)$/)[0],
      operate: "drop_file"
    }).then(() => {
      handleUpdateValue("translateOriginalMusic");
      message.success("移除成功");
    });
}

function translateClick(name) {
    sendData("config_operate", {
      fileName: name,
      type: 'myTranslate',
      operate: "drop_file"
    }).then(() => {
      handleUpdateValue("translateOriginalMusic");
      handleUpdateValue("myTranslate");
      message.success("移除成功");
    });
    sendData("config_operate", {
      fileName: name,
      type: 'translateMID',
      suffix: '.mid',
      operate: "drop_file"
    })
}

function handleFinish() {
  reloadTable();
  message.success("OK~");
}

let progressInterval: any;
function getProgress() {
  getData("getProgress").then((res) => {
    progress.tran_mid_progress = res.tran_mid_progress;
    progress.overall_progress = res.overall_progress;
    now_translate_text.text = res.now_translate_text[0];
    now_translate_text.process = res.now_translate_text[1];
  });

  if (progress.tran_mid_progress == "100.0" && progress.overall_progress == "100.0") {
    clearInterval(progressInterval);
  }
}

function handleStartTranslate() {
  if (processFlag.value) return;
  progressInterval = setInterval(getProgress, 1000);
  processFlag.value = true;
  message.success("开始转换");
  sendData("translate", {
    processor: "cpu",
  })
    .then(() => {
      reloadTable();
      message.success("转换完成");
    })
    .finally(() => {
      processFlag.value = false;
    });
}

function reloadTable() {
  handleUpdateValue("myTranslate");
  handleUpdateValue("translateOriginalMusic");
}

reloadTable();
watch(progress.overall_progress.value, () => reloadTable());

function handleUpdateValue(value: string) {
  getList(value, "").then((_res) => {
    eval("music." + value + "=_res");
  });
}
</script>

<style scoped>
:deep(.n-tabs-bar){
  --n-bar-color: rgb(242,232,196)!important;
}
:deep(.n-tabs){
    --n-tab-text-color-active: rgb(242,232,196)!important;
    --n-tab-text-color-hover: rgb(242,232,196)!important;
    --n-tab-text-color: rgb(221,242,196)!important;
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