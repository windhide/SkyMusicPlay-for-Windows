<template>
  <div class="father">
    <n-divider style="">
      <n-gradient-text
          :gradient="{
            from: 'rgb(242,201,196)',
            to: 'rgb(221,242,196)',
          }"
          id="WindHide"
        >
        AIGC Settings
      </n-gradient-text>
    </n-divider>
    <div class="father">
      <!-- <n-radio-group v-model:value="aigcValue" name="radiogroup">
        <n-space>
          <n-radio v-for="option in options" :key="option.value" :value="option.value">
            <span style="color:#F2C9C4">{{ option.label }}</span>
          </n-radio>
        </n-space>
      </n-radio-group> -->
    <n-highlight style="margin-bottom: 5px; color: #DDF2C4;" :text="headText" :patterns="patterns" :highlight-style="{
      padding: '0 6px',
      margin: '0 6px',
      borderRadius: themeVars.borderRadius,
      display: 'inline-block',
      color: 'black',
      background: '#F2C9C4',
      transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
    }" />
    <div style="flex-basis: 100%;" />
      <div style="flex-basis: 100%; margin-bottom: 20px;" />
      <n-input-group style="width:450px">
        <n-input type="text" size="large" v-model:value="token"/>
        <n-button type="primary" size="large" @click="setData()" ghost style="height:42px">
          {{ t('ai_setting.buttons.set_token') }}
        </n-button>
      </n-input-group>
      <n-button type="primary" color="#f58f98" style="height:42px; margin-left: 41px;" ghost @click="musicActive = true">
          :3
      </n-button>
    </div>
    <n-tabs
      class="card-tabs"
      default-value="signin"
      size="large"
      animated
      pane-wrapper-style="margin: 0 -4px"
      pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;"
    >
      <n-tab-pane name="signup" tab="转谱提示词">
         <n-input
            v-model:value="translate_prompt"
            type="textarea"
            placeholder="自动调整尺寸"
            :autosize="{
              minRows: 15,
              maxRows: 21
            }"
            />
      </n-tab-pane>
      <n-tab-pane name="signin" tab="延音提示词">
         <n-input
            v-model:value="duration_prompt"
            type="textarea"
            placeholder="自动调整尺寸"
            :autosize="{
              minRows: 15,
              maxRows: 21
            }"
            />
      </n-tab-pane>
    </n-tabs>
  </div>
  <n-drawer v-model:show="musicActive" :width="1000" placement="left" :trap-focus="false" :block-scroll="false">
    <n-drawer-content>
      <n-card style="margin-left: -16px; width: 965px;" :bordered="false">
        <n-tabs type="bar" animated size="small" @update:value="handleUpdateValue" @before-leave="handleBeforeLeave"
          :value="tabsNumber">
          <n-tab-pane name="systemMusic" :tab="t('tab.systemMusic')">
            <n-data-table :columns="tableColumns" :data="music.systemMusic" :bordered="false" :min-row-height="48"
              ref="systemMusic" :max-height="600" :virtual-scroll="music.systemMusic?.length > 7"
              :row-class-name="rowClassName" style="
              --n-td-color: rgba(57, 57, 62, 0);
              --n-th-color-hover: rgba(57, 57, 62, 0);
              --n-th-color: rgba(57, 57, 62, 0);
              --n-td-color-hover: rgba(0, 0, 0, 0.2);
            " />
          </n-tab-pane>
          <n-tab-pane name="myImport" :tab="t('tab.myImport')" ref="myImport">
            <n-data-table :columns="tableColumns" :data="music.myImport" :bordered="false" :min-row-height="48"
              ref="myImport" :max-height="600" :virtual-scroll="music.myImport?.length > 7"
              :row-class-name="rowClassName" style="
              --n-td-color: rgba(57, 57, 62, 0);
              --n-th-color-hover: rgba(57, 57, 62, 0);
              --n-th-color: rgba(57, 57, 62, 0);
              --n-td-color-hover: rgba(0, 0, 0, 0.2);
            " />
          </n-tab-pane>
          <n-tab-pane name="myTranslate" :tab="t('tab.myTranslate')" ref="myTranslate">
            <n-data-table :columns="tableColumns" :data="music.myTranslate" :bordered="false" :min-row-height="48"
              ref="myTranslate" :max-height="600" :virtual-scroll="music.myTranslate?.length > 7"
              :row-class-name="rowClassName" style="
              --n-td-color: rgba(57, 57, 62, 0);
              --n-th-color-hover: rgba(57, 57, 62, 0);
              --n-th-color: rgba(57, 57, 62, 0);
              --n-td-color-hover: rgba(0, 0, 0, 0.2);
            " />
          </n-tab-pane>
          <n-tab-pane name="myFavorite" :tab="t('tab.myFavorite')" ref="myFavorite">
            <n-data-table :columns="tableColumns" :data="music.myFavorite" :bordered="false" :min-row-height="48"
              ref="myFavorite" :max-height="600" :virtual-scroll="music.myFavorite?.length > 7"
              :row-class-name="rowClassName" style="
              --n-td-color: rgba(57, 57, 62, 0);
              --n-th-color-hover: rgba(57, 57, 62, 0);
              --n-th-color: rgba(57, 57, 62, 0);
              --n-td-color-hover: rgba(0, 0, 0, 0.2);
            " />
          </n-tab-pane>
          <template #suffix>
            <n-input v-model:value="searchText" round :placeholder="t('tab.search')" style="top:-3px;width: 25vh; margin-left: 5px">
              <template #suffix>
                <n-icon :component="Search" />
              </template>
            </n-input>
          </template>
        </n-tabs>
      </n-card>
    </n-drawer-content>
  </n-drawer>
</template>

<script setup lang="ts">
import { getList, sendData } from "@renderer/utils/fetchUtils";
import { h, onMounted, onUnmounted, reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { MessageReactive, NButton, useMessage, useThemeVars } from 'naive-ui'
import { RowData } from "naive-ui/es/data-table/src/interface";
import { Search } from '@vicons/ionicons5'
import { debounce } from "lodash-es";
const themeVars = useThemeVars();
const { t } = useI18n();
const message = useMessage()
let messageReactive: MessageReactive | null = null
const token = ref("")
const translate_prompt = ref("")
const duration_prompt = ref("")
const musicActive = ref(false);
const tabsNumber = ref("systemMusic")
const searchText = ref('');
let aigcValue = ref("DeepSeek")
const QCount = ref(300)
const headText = "音乐时间过长，需要等待的时间也就越长。频繁失败代表api没钱了，aigc出来的效果未必很好，请不要抱有太大期望，api没钱了可以去DeepSeek官网申请自行在下方保存"
const patterns = ["没钱了","等待","越长","效果未必很好", "期望", "没钱了", "DeepSeek", "申请", "保存"]
const options = [
  {
    label: "DeepSeek（AI也会犯错效果不会那么好）",
    value: 'DeepSeek'
  },
  // {
  //   label: "Kimi",
  //   value: 'Kimi'
  // },
  // {
  //   label: "Qwen",
  //   value: 'Qwen'
  // }
]
let nowType = 'systemMusic'
// 音乐数据管理
const music: any = reactive({
  systemMusic: [],
  myImport: [],
  myTranslate: [],
  myFavorite: [],
  musicList: []
});
const fetchListData = debounce(() => {
  getListData('myFavorite');
  getListData('systemMusic');
  getListData('myImport');
  getListData('myTranslate');
}, 200);
watch(searchText, fetchListData)
function handleBeforeLeave(name: string) {
  nowType = name
  return true
}
function rowClassName(row: RowData) {
  if (row?.position) {
    return 'table_position'
  }
  return 'td_css'
}
function setData(){
  sendData("config_operate", {
    "operate": "set",
    "name": "ai_token",
    "value": {
      "type": aigcValue.value,
      "token":token.value
    }
  })
  sendData("config_operate", {
    "operate": "set",
    "name": "translate_prompt",
    "value": translate_prompt.value
  })
  sendData("config_operate", {
    "operate": "set",
    "name": "duration_prompt",
    "value": duration_prompt.value
  })
  message.success("done")
  getData()
}

function getData(){
  sendData("config_operate",{
    "operate":"get",
    "name": `general_ai`
  }).then(res=>{
    token.value = res[aigcValue.value]["key"]
  })
  sendData("config_operate",{
    "operate":"get",
    "name": "translate_prompt"
  }).then(res=>{
    translate_prompt.value = res
  })
  sendData("config_operate",{
    "operate":"get",
    "name": "duration_prompt"
  }).then(res=>{
    duration_prompt.value = res
  })
}
watch(translate_prompt, () => {
  sendData("config_operate", {
    "operate": "set",
    "name": "translate_prompt",
    "value": translate_prompt.value
  })
})
watch(duration_prompt, () => {
  sendData("config_operate", {
    "operate": "set",
    "name": "duration_prompt",
    "value": duration_prompt.value
  })
})

const tableColumns = [
  {
    title: t('columns.name'),
    key: 'name',
    resizable: true,
    className: 'th_css',
    ellipsis: { tooltip: true }
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
    align: "center",
    width: 150,
    className: 'th_css',
    render(row) {
      return [
        h(NButton, {
        ghost: true,
        onClick: () => {
          messageReactive = message.loading(`正在调用${aigcValue.value}进行优化曲谱`, {
            duration: 0
          })
          sendData("aigc", {
             "ai": aigcValue.value,
             "model": "duration",
             "filename": row.truthName,
             "type": nowType 
            }).then(_res => {
              if (_res == "ok"){
                messageReactive!.destroy()
                messageReactive = null
                message.success('保存到了已转换歌曲下了~', {
                  duration: 5000
                })
              }else{
                messageReactive!.destroy()
                messageReactive = null
                message.error('一定是那里出问题了，可能吧？', {
                  duration: 5000
                })
              }
            }).catch(_=>{
                message.error('一定是哪里出问题了，可能吧？', {
                  duration: 5000
                })
            })
        }
      }, {
        default: () => '🎻'
      }),
      h(NButton, {
        size: 'medium',
        ghost: true,
        onClick: () => {
          messageReactive = message.loading(`正在调用${aigcValue.value}进行优化曲谱`, {
            duration: 0
          })
          sendData("aigc", {
              "ai": aigcValue.value,
              "model": "optimization",
              "filename": row.truthName,
              "type": nowType 
            }).then(_res => {
              if (_res == "ok"){
                messageReactive!.destroy()
                messageReactive = null
                message.success('保存到了已转换歌曲下了~', {
                  duration: 5000
                })
              }else{
                messageReactive!.destroy()
                messageReactive = null
                message.error('一定是哪里出问题了，可能吧？', {
                  duration: 5000
                })
              }
            }).catch(_=>{
                message.error('一定是哪里出问题了，可能吧？', {
                  duration: 5000
                })
            })
        },
        style: {
          marginLeft: '10px',       // 设置边框圆角
        }
      }, {
        default: () => '🎹'
      })
      ]
    }
  }
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

function handleUpdateValue(value: string) {
  tabsNumber.value = value
  getListData(value)
}

async function getListData(value) {
  await getList(value, searchText.value).then((_res) => {
    eval('music.' + value + '=_res')
  })
}

watch(aigcValue, getData)

onMounted(()=>{
  getData()
  window.api.window_size(774, 1500);
  getListData('systemMusic');
})
onUnmounted(()=>{
  window.api.window_size(0, 0);
})
</script>

<style scoped>
@import url(https://fonts.googleapis.com/css?family=Pacifico);

.father{
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  flex-wrap: wrap; /* 允许换行 */
}
#WindHide {
  font-size: 30px;
  font-weight: bolder;
  font-family: "pacifico";
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
.n-input{
  background-color: rgba(24, 24, 28, 0) !important;
  border: 1pt solid rgba(242,232,196,0.5);
}

.midi-canvas {
  width: 100%;
  height: 100%;
  display: block;
  background: transparent;
}

:deep(.n-input) {
  --n-border-hover: 1px solid rgb(242, 232, 196) !important;
  --n-border-focus: 1px solid rgb(242, 232, 196) !important;
  --n-caret-color: rgb(242, 232, 196) !important;
  --n-color-focus: rgba(242, 232, 196, 0.1) !important;
  --n-text-color: rgb(242,232,196) !important;
}

:deep(.td_css td) {
  color: rgb(242, 232, 196) !important;
}

:deep(.th_css) {
  color: rgb(221, 242, 196) !important;
}
:deep(.n-base-selection-label){
  height:5.4vh !important;
}

:deep(.n-radio){
  --n-box-shadow-active: inset 0 0 0 1px rgb(242,232,196)!important;
  --n-box-shadow-focus: inset 0 0 0 1px rgb(242,232,196), 0 0 0 2px rgba(242,232,196, 0.3)!important;
  --n-box-shadow-hover: inset 0 0 0 1px rgb(242,232,196)!important;
  --n-dot-color-active: rgb(242,232,196)!important;
}
</style>
