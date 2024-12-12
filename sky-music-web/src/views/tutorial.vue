<template>
  <n-flex align="center">
    <n-gradient-text :size="20" type="success" style="width: 100%">
      {{ "当前: " + nowPlayMusic + "" }}
    </n-gradient-text>
    <n-button type="primary" ghost @Click="followTutorial">
      开始跟弹
    </n-button>
  </n-flex>
  <n-card style="margin-top: 20px">
    <n-tabs type="bar" animated @update:value="handleUpdateValue" size="small">
      <n-tab-pane name="systemMusic" tab="自带歌曲">
        <n-data-table :columns="musicColumns" :data="music.systemMusic" :bordered="false" :max-height="301"
          :scroll-x="100" :row-props="systemMusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myImport" tab="导入的歌曲">
        <n-data-table :columns="musicColumns" :data="music.myImport" :bordered="false" :max-height="300" :scroll-x="100"
          :row-props="myImportMusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="转换的歌曲">
        <n-data-table :columns="musicColumns" :data="music.myTranslate" :bordered="false" :max-height="250"
          :scroll-x="100" :row-props="myTranslateMusicSelect" />
      </n-tab-pane>
      <n-tab-pane name="myFavorite" tab="收藏">
        <n-data-table :columns="musicColumns" :data="music.myFavorite" :bordered="false" :max-height="250"
          :row-props="myFavoriteMusicSelect" />
      </n-tab-pane>
      <template #suffix>
        <n-input round placeholder="搜索" v-model:value="searchText" style="margin-bottom: 5px; width: 25vh;">
          <template #suffix>
            <n-icon :component="Search" />
          </template>
        </n-input>
      </template>
    </n-tabs>
  </n-card>
</template>

<script lang="ts" setup>
import { getList, sendData } from "@/utils/fetchUtils";
import { RowData } from "naive-ui/es/data-table/src/interface";
import { reactive, ref, watch } from "vue";
import { useMessage } from 'naive-ui'
import { Search } from '@vicons/ionicons5'

const message = useMessage()


let music: any = reactive({
  // 音乐列表
  systemMusic: [], // 原版音乐
  myImport: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
});
let nowPlayMusic = ref("没有歌曲"); // 当前选中歌曲
let nowType = ""
let searchText = ref("")
let musicColumns = [
  {
    title: "歌名",
    key: "name",
  },
]; // 音乐列

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

function handleUpdateValue(value: string) {
  searchText.value = ""
  getList(value).then(res => {
    eval("music." + value + "=res")
  })
}
const myFavoriteMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
      nowType = "myFavorite"
    },
  };
};

watch(searchText, () => {
  if (searchText.value === "" || searchText.value === undefined || searchText.value === null) {
    handleUpdateValue("systemMusic")
    handleUpdateValue("myImport")
    handleUpdateValue("myTranslate")
    handleUpdateValue("myFavorite")
    return
  }
  music.systemMusic = music.systemMusic.filter((res) => { return res.name.includes(searchText.value) })
  music.myImport = music.myImport.filter((res) => { return res.name.includes(searchText.value) })
  music.myTranslate = music.myTranslate.filter((res) => { return res.name.includes(searchText.value) })
  music.myFavorite = music.myFavorite.filter((res) => { return res.name.includes(searchText.value) })
})

function followTutorial() {
  if (nowPlayMusic.value === "没有歌曲") {
    message.error("选个歌再跟弹吧靓仔")
    return;
  } else {
    sendData("followSheet", {
      fileName: nowPlayMusic.value,
      type: nowType
    }).then(() => {
      window.open("app://./index.html" ,"_blank", "toolbar=yes, location=yes, directories=no, status=no, menubar=yes, scrollbars=yes, resizable=no, copyhistory=yes, width=600, height=400");
    })
  }
}
handleUpdateValue("systemMusic")
</script>
