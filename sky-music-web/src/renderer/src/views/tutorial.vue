<template>
  <n-flex align="center">
    <n-gradient-text :size="20" type="success" style="width: 100%; color: #f2e8c4">
      {{ t('tutorial.now', { music:nowPlayMusic }) }}
    </n-gradient-text>
    <n-button type="primary" ghost @click="followTutorial" color="#F2C9C4">
      {{ t('tutorial.follow') }}
    </n-button>
    <n-button type="primary" ghost :loading="processFlag" @click="transfer" color="#F2E8C4">{{ t('tutorial.save') }}</n-button>
  </n-flex>
  <n-card  style="margin-left: -22px; width: 640px;" :bordered="false">
    <n-tabs
      type="bar"
      animated
      size="small"
      @update:value="handleUpdateValue"
      @before-leave="handleBeforeLeave"
    >
      <n-tab-pane name="systemMusic" :tab="t('tab.systemMusic')">
        <n-data-table
          :columns="musicSystemColumns"
          :data="music.systemMusic"
          :bordered="false"
          :min-row-height="48"
          :max-height="490"
          :virtual-scroll="music.systemMusic?.length > 7"
          :row-props="MusicSelect"
          row-class-name="td_css"
          style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <n-tab-pane name="myImport" :tab="t('tab.myImport')">
        <n-data-table
          :columns="musicColumns"
          :data="music.myImport"
          :bordered="false"
          :min-row-height="48"
          :max-height="490"
          :virtual-scroll="music.myImport?.length > 7"
          :row-props="MusicSelect"
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
          :columns="musicColumns"
          :data="music.myTranslate"
          :bordered="false"
          :min-row-height="48"
          :max-height="490"
          :virtual-scroll="music.myTranslate?.length > 7"
          :row-props="MusicSelect"
          row-class-name="td_css"
          style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <n-tab-pane name="myFavorite" :tab="t('tab.myFavorite')">
        <n-data-table
          :columns="favoritColumns"
          :data="music.myFavorite"
          :bordered="false"
          :min-row-height="48"
          :max-height="490"
          :virtual-scroll="music.myFavorite?.length > 7"
          :row-props="MusicSelect"
          row-class-name="td_css"
          style="
            --n-td-color: rgba(57, 57, 62, 0);
            --n-th-color-hover: rgba(57, 57, 62, 0);
            --n-th-color: rgba(57, 57, 62, 0);
            --n-td-color-hover: rgba(0, 0, 0, 0.2);
          "/>
      </n-tab-pane>
      <template #suffix>
        <n-input
          v-model:value="searchText"
          round
          :placeholder="t('tab.search')"
          style="top: -4px; width: 25vh; margin-left: 5px"
        >
          <template #suffix>
            <n-icon :component="Search" />
          </template>
        </n-input>
      </template>
    </n-tabs>
  </n-card>
</template>

<script lang="ts" setup>
import { getList, sendData } from "@renderer/utils/fetchUtils";
import { RowData } from "naive-ui/es/data-table/src/interface";
import { h, reactive, ref, watch } from "vue";
import { useMessage, NButton } from "naive-ui";
import { Search } from "@vicons/ionicons5";
import { debounce } from "lodash-es";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const message = useMessage();

const music: any = reactive({
  // 音乐列表
  systemMusic: [], // 原版音乐
  myImport: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
  myFavorite: [],
});
const nowPlayMusic = ref(t('tutorial.no_music')); // 当前选中歌曲
const nowSelectMusicTruth = ref('') // 当前选中歌曲真实名称
let nowType = "systemMusic";
const searchText = ref("");
const musicColumns = [
  {
    title: t("columns.name"),
    key: "name",
    className: "th_css",
    resizable: true,
  },
  {
    title: t("columns.total_duration"),
    key: 'total_duration',
    width: 80,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    },
    sorter: (row1, row2) => timeToSeconds(row1.total_duration) - timeToSeconds(row2.total_duration)
  },
]; // 音乐列

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

// 进程标记
const processFlag = ref(false)

/**
 * 发送扒谱转换请求
 */
 async function transfer() {
  if (nowPlayMusic.value === t("tutorial.no_music")) {
    message.warning(t("tutorial.chose_music"))
    return
  }

  try {
    await sendData('config_operate', {
      fileName: nowSelectMusicTruth.value,
      type: nowType,
      operate: 'convert_sheet'
    })
    message.success(t("tutorial.save_desktop"))
  } catch (error) {
    console.error(t("tutorial.error_console"), error)
    message.error(t("tutorial.error"))
  }
}


const musicSystemColumns = [
  {
    title: t("columns.name"),
    key: 'name',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: t("columns.total_duration"),
    key: 'total_duration',
    width: 80,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    },
    sorter: (row1, row2) => timeToSeconds(row1.total_duration) - timeToSeconds(row2.total_duration)
  },
  {
    title: t("columns.operation"),
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
              return res.name.replaceAll('.mp3').includes(row.name)
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
    title: t("columns.name"),
    key: 'name',
    resizable: true,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: t("columns.total_duration"),
    key: 'total_duration',
    width: 80,
    className: 'th_css',
    ellipsis: {
      tooltip: true
    },
    sorter: (row1, row2) => timeToSeconds(row1.total_duration) - timeToSeconds(row2.total_duration)
  },
  {
    title: t("columns.operation"),
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
      message.success(t("tab.love_success"))
    })
  } else {
    sendData('config_operate', {
      fileName: name,
      type: 'myFavorite',
      operate: "drop_file"
    }).then(() => {
      handleUpdateValue('myFavorite')
      message.success(t("tab.remove_success"))
    })
  }
}

const MusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
      nowSelectMusicTruth.value = row.truthName;
    },
  };
};

function handleUpdateValue(value: string) {
  searchText.value = "";
  getListData(value);
}

function handleBeforeLeave(name: string) {
  nowType = name;
  return true;
}

const fetchListData = debounce(() => {
  getListData('myFavorite');
  getListData('systemMusic');
  getListData('myImport');
  getListData('myTranslate');
}, 200);
watch(searchText, fetchListData)

function followTutorial() {
  if (nowPlayMusic.value === t("tutorial.no_music")) {
    message.error(t("messeage.choose_plz"));
    return;
  } else {
    sendData("follow", {
      fileName: nowSelectMusicTruth.value,
      type: nowType,
      operate: "setSheet",
    }).then(() => {
      sendData("follow", {
        operate: "openFollow",
      });
    });
  }
}
handleUpdateValue("myFavorite");
handleUpdateValue("systemMusic");

function getListData(value) {
  getList(value, searchText.value).then((_res) => {
    eval("music." + value + "=_res");
  });
}
</script>

<style scoped>
:deep(.n-tabs-bar) {
  --n-bar-color: rgb(242, 232, 196) !important;
}
:deep(.n-tabs) {
  --n-tab-text-color-active: rgb(242, 232, 196) !important;
  --n-tab-text-color-hover: rgb(242, 232, 196) !important;
  --n-tab-text-color: rgb(221, 242, 196) !important;
}
.n-input {
  background-color: rgba(24, 24, 28, 0) !important;
  border: 1px solid rgba(242, 232, 196, 0.5);
}
:deep(.n-input){
  --n-border-hover: 1px solid rgb(242,232,196)!important;
  --n-border-focus: 1px solid rgb(242,232,196)!important;
  --n-caret-color: rgb(242,232,196)!important;
  --n-color-focus: rgba(242,232,196,0.1)!important;
  --n-text-color: rgb(242,232,196) !important;
}
:deep(.td_css td) {
  color: rgb(242, 232, 196) !important;
}
:deep(.th_css) {
  color: rgb(221, 242, 196) !important;
}
</style>
