<template>
  <n-flex align="center">
    <n-gradient-text :size="24" type="success" style="width: 100%; color:#F2E8C4">
      转换歌曲
    </n-gradient-text>
    <n-upload
      action="http://localhost:9899/fileUpload"
      multiple
      style="width: 100px; height: 34px"
      accept=".mp3,.flac,.wav,.m4a,.ogg,.mid"
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
const progressInterval = ref<number | null>(null);


function handleFinish() {
  reloadTable()
  message.success('OK~')
}

const music = reactive({
  translateOriginalMusic: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
});

const progress = reactive({
  overall_progress: 0,
});

const now_translate_text = reactive({
  process: "",
  text: "",
});

const originalColumns = [
  {
    title: "歌名",
    key: "name",
    className: "th_css",
  },
  {
    title: "操作",
    key: "operation",
    width: 100,
    className: "th_css",
    render(row) {
      return h(
        NButton,
        {
          size: "medium",
          text: true,
          onClick: () => originalClick(row.name),
        },
        { default: () => "❌" }
      );
    },
  },
];

const translateColumns = [
  {
    title: "歌名",
    key: "name",
    className: "th_css",
  },
  {
    title: "操作",
    key: "operation",
    width: 100,
    className: "th_css",
    render(row) {
      return h(
        NButton,
        {
          size: "medium",
          text: true,
          onClick: () => translateClick(row.name),
        },
        { default: () => "❌" }
      );
    },
  },
];

/**
 * 处理原始音乐删除
 */
async function originalClick(name: string) {
  try {
    const baseName = name.slice(0, name.lastIndexOf("."));
    const suffix = name.match(/(\.[^.]*)$/)?.[0] || "";

    await sendData("config_operate", {
      fileName: baseName,
      type: "translateOriginalMusic",
      suffix,
      operate: "drop_file",
    });

    await sendData("config_operate", {
      fileName: baseName.replace("_ok", "_basic_pitch"),
      type: "translateMID",
      suffix: ".mid",
      operate: "drop_file",
    });

    handleUpdateValue("translateOriginalMusic");
    message.success("移除成功");
  } catch (error) {
    console.error("删除失败:", error);
  }
}

/**
 * 处理扒谱音乐删除
 */
async function translateClick(name: string) {
  try {
    await sendData("config_operate", {
      fileName: name,
      type: "myTranslate",
      operate: "drop_file",
    });

    handleUpdateValue("translateOriginalMusic");
    handleUpdateValue("myTranslate");
    message.success("移除成功");
  } catch (error) {
    console.error("删除失败:", error);
  }
}

/**
 * 获取转换进度
 */
async function getProgress() {
  try {
    const res = await getData("getProgress");
    progress.overall_progress = res.overall_progress;
    now_translate_text.text = res.now_translate_text?.[0] || "";
    now_translate_text.process = res.now_translate_text?.[1] || "";

    if (""+progress.overall_progress === "100.0") {
      if (progressInterval.value) {
        clearInterval(progressInterval.value);
        progressInterval.value = null;
      }
    }
  } catch (error) {
    console.error("获取进度失败:", error);
  }
}

/**
 * 开始扒谱转换
 */
async function handleStartTranslate() {
  if (processFlag.value) return;
  processFlag.value = true;
  message.success("开始转换");

  if (!progressInterval.value) {
    progressInterval.value = setInterval(getProgress, 1000) as unknown as number;
  }

  try {
    await sendData("translate", { operate: "translate" });
    reloadTable();
    message.success("转换完成");
  } catch (error) {
    console.error("转换失败:", error);
  } finally {
    processFlag.value = false;
  }
}

/**
 * 重新加载表格数据
 */
function reloadTable() {
  handleUpdateValue("myTranslate");
  handleUpdateValue("translateOriginalMusic");
}

/**
 * 监听进度变化，自动更新表格
 */
watch(
  () => progress.overall_progress,
  () => {
    if (""+progress.overall_progress === "100.0") {
      reloadTable();
    }
  }
);

/**
 * 更新音乐列表数据
 */
async function handleUpdateValue(value: keyof typeof music) {
  try {
    const res = await getList(value, "");
    music[value] = res;
  } catch (error) {
    console.error(`获取 ${value} 失败:`, error);
  }
}

reloadTable();
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