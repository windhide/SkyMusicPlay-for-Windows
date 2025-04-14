<template>
  <n-flex align="center">
    <n-gradient-text :size="24" type="success" style="width: 100%; color:#F2E8C4">
      {{ t("kube.title") }} 
    </n-gradient-text>
    <n-upload
      action="http://localhost:9899/fileUpload"
      multiple
      style="width: 100px; height: 34px"
      accept=".mp3,.flac,.wav,.m4a,.ogg,.mid"
      :show-file-list="false"
      @finish="handleFinish"
    >
    <n-button type="info" ghost color="#F2C9C4"> {{ t("kube.chose_music") }} 
      <template #icon>
        <n-icon size="25px"><CloudArrowUp32Filled /></n-icon>
      </template>
    </n-button>
    </n-upload>
    <n-button type="primary" ghost :loading="processFlag" @click="handleStartTranslate" style="margin-left: 7px;" color="#F2E8C4">
      {{ t("kube.star_transfer") }} 
      <template #icon>
        <n-icon size="25px"><ArrowSync24Regular /></n-icon>
      </template>
    </n-button>
    <n-switch size="medium" v-model:value="isSingular" @update:value="singularChange" :rail-style="railStyle" :round="false"> 
        <template #checked-icon>
          🤔
        </template>
        <template #unchecked-icon>
          🧐
        </template>
        <template #checked>
          <p style="color: rgba(94, 104, 81, 1);">{{ t("kube.odd") }} </p>
        </template>
        <template #unchecked>
          <p style="color: rgba(94, 104, 81, 1);">{{ t("kube.dual") }} </p>
        </template>
    </n-switch>
    <n-switch size="medium" v-model:value="semitone_switch" @update:value="semitoneChange" :rail-style="railStyle" :round="false"> 
        <template #checked-icon>
          🤔
        </template>
        <template #unchecked-icon>
          🧐
        </template>
        <template #checked>
          <p style="color: rgba(94, 104, 81, 1);">{{ t("kube.half_t") }}</p>
        </template>
        <template #unchecked>
          <p style="color: rgba(94, 104, 81, 1);">{{ t("kube.all_t") }}</p>
        </template>
    </n-switch>
    <n-switch size="medium" v-model:value="detail_switch" @update:value="detailChange" :rail-style="railStyle" :round="false"> 
        <template #checked-icon>
          🤔
        </template>
        <template #unchecked-icon>
          🧐
        </template>
        <template #checked>
          <p style="color: rgba(94, 104, 81, 1);">{{ t("kube.other_key") }}</p>
        </template>
        <template #unchecked>
          <p style="color: rgba(94, 104, 81, 1);">{{ t("kube.range_key") }}</p>
        </template>
    </n-switch>
    <div style="flex-basis: 100%;" />
    <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">
      {{ t("kube.Streng_filter") }}
    </n-gradient-text>
    <n-input-number v-model:value="velocity_filter" style="flex-basis: 20%;" />
    <div style="flex-basis: 100%;" />
    <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">
      {{ t("kube.dynamic_merge") }}
    </n-gradient-text>
    <n-input-number v-model:value="merge_min" style="flex-basis: 20%;"/>
    <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))">
      -
    </n-gradient-text>
    <n-input-number v-model:value="merge_max" style="flex-basis: 20%;"/>
    <n-checkbox-group v-model:value="chooseType" style="margin-left: 1px; margin-top: 5px;">
        <n-space item-style="display: flex;">
          <n-checkbox value="2" :label="t('kube.scale.scale2')" />
          <n-checkbox value="3" :label="t('kube.scale.scale3')" />
          <n-checkbox value="4" :label="t('kube.scale.scale4')" />
          <n-checkbox value="5" :label="t('kube.scale.scale5')" />
          <n-checkbox value="6" :label="t('kube.scale.scale6')" />
        </n-space>
    </n-checkbox-group>
    <n-divider style="margin:0px"/>
    <div style="flex-basis: 100%;" />
    <n-gradient-text type="info" style="color: #F2C9C4; flex-basis: 10%"> {{ t("kube.transfer_progress") }} </n-gradient-text>
    <n-progress
      color="#F2C9C4"
      style="flex-basis: 80%"
      type="line"
      :percentage="progress.overall_progress"
      indicator-placement="inside"
      processing
    />
  </n-flex>

  <n-card style="margin-left: -22px; width: 640px;" :bordered="false">
    <n-tabs type="line" animated @update:value="handleUpdateValue">
      <n-tab-pane name="translateOriginalMusic" :tab="t('tab.translateOriginalMusic')">
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
      <n-tab-pane name="myTranslate" :tab="t('tab.myTranslate')">
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
import { h, onUnmounted, reactive, ref, watch, CSSProperties } from "vue";
import { NButton, useMessage } from "naive-ui";
import {
  CloudArrowUp32Filled,
  ArrowSync24Regular
} from '@vicons/fluent'
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const message = useMessage();
const processFlag = ref(false);
let progressInterval:any = null
let chooseType:any = ref(['2'])
let isSingular = ref(true)
let semitone_switch = ref(true)
let detail_switch = ref(true)

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
    title: t('columns.name'),
    key: "name",
    className: "th_css",
  },
  {
    title: t('columns.operation'),
    key: "operation",
    width: 100,
    className: "th_css",
    render(row) {
      return h(
        NButton,
        {
          size: "medium",
          text: true,
          onClick: () => {
            originalClick(row.name)
            window.api.sync_sheet_2_el()
          }
        },
        { default: () => "❌" }
      );
    },
  },
];

const translateColumns = [
  {
    title: t('columns.name'),
    key: "name",
    className: "th_css",
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
    key: "operation",
    width: 100,
    className: "th_css",
    render(row) {
      return h(
        NButton,
        {
          size: "medium",
          text: true,
          onClick: () => {
            translateClick(row.truthName)
            window.api.sync_sheet_2_el()
          }
        },
        { default: () => "❌" }
      );
    },
  },
];

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


function railStyle({ focused, checked }){
  const style: CSSProperties = {}
  if (checked) {
    style.background = '#F2C9C4'
    if (focused) {
      style.boxShadow = '0 0 0 2px #F2C9C440'
    }
  }
  else {
    style.background = '#F2E8C4'
    if (focused) {
      style.boxShadow = '0 0 0 2px #F2E8C440'
    }
  }
  return style
}


function singularChange(value: boolean){
  sendData("config_operate",{
    operate: "set",
    name: "is_singular",
    value
  })
}
function detailChange(value: boolean){
  sendData("config_operate",{
    operate: "set",
    name: "detail_switch",
    value
  })
}
function semitoneChange(value: boolean){
  sendData("config_operate",{
    operate: "set",
    name: "semitone_switch",
    value
  })
}

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
    message.success(t('messeage.remove_success'));
  } catch (error) {
    console.error(t('messeage.remove_fail'), error);
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
    message.success(t('messeage.remove_success'));
  } catch (error) {
    console.error(t('messeage.remove_fail'), error);
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
    console.error(t('messeage.progress_fail'), error);
  }
}

/**
 * 开始扒谱转换
 */
async function handleStartTranslate() {
  if (processFlag.value) return;
  processFlag.value = true;
  message.success(t('kube.star_transfer'));

  if (!progressInterval) {
    progressInterval = setInterval(getProgress, 1000) as unknown as number;
  }

  try {
    await sendData("translate", { operate: "translate", value: chooseType.value.join() });
    reloadTable();
    message.success(t('kube.transfer_success'));
  } catch (error) {
    console.error(t('kube.transfer_fail'), error);
  } finally {
    processFlag.value = false;
    window.api.sync_sheet_2_el()
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
    console.error(t('kube.get_fail', {value}), error);
  }
}

reloadTable();

sendData("config_operate",{ operate: "get", name: "detail_switch"}).then(res=>{ detail_switch.value=res})
sendData("config_operate",{ operate: "get", name: "semitone_switch"}).then(res=>{ semitone_switch.value=res})
sendData("config_operate",{ operate: "get", name: "velocity_filter"}).then(res=>{ velocity_filter.value=res})
sendData("config_operate",{ operate: "get", name: "merge_max"}).then(res=>{ merge_max.value=res})
sendData("config_operate",{ operate: "get", name: "merge_min"}).then(res=>{ merge_min.value=res})

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
:deep(.n-input){
  --n-border-hover: 1px solid rgb(242,232,196)!important;
  --n-border-focus: 1px solid rgb(242,232,196)!important;
  --n-caret-color: rgb(242,232,196)!important;
  --n-color-focus: rgba(242,232,196,0.1)!important;
}
</style>