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
    <div style="flex-basis: 100%;" />
    <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">
      力度过滤(低于毫秒)：
    </n-gradient-text>
    <n-input-number v-model:value="velocity_filter" style="flex-basis: 20%;" />
    <div style="flex-basis: 100%;" />
    <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">
      动态合并阈值范围划分（动态取决于bmp计算）
    </n-gradient-text>
    <n-input-number v-model:value="merge_min" style="flex-basis: 20%;"/>
    <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">
      -
    </n-gradient-text>
    <n-input-number v-model:value="merge_max" style="flex-basis: 20%;"/>
    <n-checkbox-group v-model:value="chooseType" style="margin-left: 1px; margin-top: 5px;">
        <n-space item-style="display: flex;">
          <n-checkbox value="2" label="光遇范围_2组音阶" />
          <n-checkbox value="3" label="3组音阶" />
          <n-checkbox value="4" label="4组音阶" />
          <n-checkbox value="5" label="5组音阶" />
          <n-checkbox value="6" label="6组音阶" />
        </n-space>
    </n-checkbox-group>
    <n-divider style="margin:0px"/>
    <div style="flex-basis: 100%;" />
    <n-gradient-text type="info" style="color: #F2C9C4; flex-basis: 10%"> 转换进度 </n-gradient-text>
    <n-progress
      color="#F2C9C4"
      style="flex-basis: 80%"
      type="line"
      :percentage="progress.overall_progress"
      indicator-placement="inside"
      processing
    />
  </n-flex>

  <n-card style="margin-left: -22px;" :bordered="false">
    <n-tabs type="line" animated @update:value="handleUpdateValue">
      <n-tab-pane name="translateOriginalMusic" tab="未转换歌曲">
        <n-data-table
          :columns="originalColumns"
          :data="music.translateOriginalMusic"
          :bordered="false"
          :max-height="290"
          :scroll-x="100"
          row-class-name="td_css"
          style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="已转换歌曲">
        <n-data-table
          :columns="translateColumns"
          :data="music.myTranslate"
          :bordered="false"
          :max-height="290"
          :scroll-x="100"
          row-class-name="td_css"
          style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>

<script lang="ts" setup>
import { getData, sendData, getList, setConfig } from "@renderer/utils/fetchUtils";
import { h, onUnmounted, reactive, ref, watch } from "vue";
import { NButton, useMessage } from "naive-ui";

const message = useMessage();
const processFlag = ref(false);
let progressInterval:any = null
let chooseType:any = ref(['2'])

let merge_min = ref(20)
let merge_max = ref(30)
let velocity_filter = ref(10)


watch(merge_min, ()=>{ setConfig('merge_min', merge_min.value)})
watch(merge_max, ()=>{ setConfig('merge_max', merge_max.value)})
watch(velocity_filter, ()=>{ setConfig('velocity_filter', velocity_filter.value)})
sendData("config_operate",{ "operate": "get", "name": "merge_min"}).then(res=>{ merge_min.value=res})
sendData("config_operate",{ "operate": "get", "name": "merge_max"}).then(res=>{ merge_max.value=res})
sendData("config_operate",{ "operate": "get", "name": "velocity_filter"}).then(res=>{ velocity_filter.value=res})

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
      if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
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

  if (!progressInterval) {
    progressInterval = setInterval(getProgress, 1000) as unknown as number;
  }

  try {
    await sendData("translate", { operate: "translate", value: chooseType.value.join() });
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

onUnmounted(function(){
  clearInterval(progressInterval);
})

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
:deep(.n-checkbox){
  --n-color-checked: rgb(242,232,196)!important;
  --n-border-checked: 1px solid #F2C9C4 !important;
  --n-border-focus: 1px solid #F2C9C4 !important;
  --n-text-color: #F2C9C4 !important;
}
</style>