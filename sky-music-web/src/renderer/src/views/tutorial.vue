<template>
  <n-flex align="center">
    <n-gradient-text :size="20" type="success" style="width: 100%">
      {{ '当前: ' + nowPlayMusic + '' }}
    </n-gradient-text>
    <n-button type="primary" ghost @click="followTutorial"> 开始跟弹 </n-button>
  </n-flex>
  <n-card style="margin-top: 20px">
    <n-tabs
      type="bar"
      animated
      size="small"
      @update:value="handleUpdateValue"
      @before-leave="handleBeforeLeave"
    >
      <n-tab-pane name="systemMusic" tab="自带歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.systemMusic"
          :bordered="false"
          :min-row-height="48"
          :max-height="300"
          :virtual-scroll="music.systemMusic.length > 7"
          :row-props="systemMusicSelect"
        />
      </n-tab-pane>
      <n-tab-pane name="myImport" tab="导入歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.myImport"
          :bordered="false"
          :min-row-height="48"
          :max-height="300"
          :virtual-scroll="music.myImport.length > 7"
          :row-props="myImportMusicSelect"
        />
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="转换歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.myTranslate"
          :bordered="false"
          :min-row-height="48"
          :max-height="300"
          :virtual-scroll="music.myTranslate.length > 7"
          :row-props="myTranslateMusicSelect"
        />
      </n-tab-pane>
      <n-tab-pane name="myFavorite" tab="收藏">
        <n-data-table
          :columns="musicColumns"
          :data="music.myFavorite"
          :bordered="false"
          :min-row-height="48"
          :max-height="300"
          :virtual-scroll="music.myFavorite.length > 7"
          :row-props="myFavoriteMusicSelect"
        />
      </n-tab-pane>
      <template #suffix>
        <n-input
          v-model:value="searchText"
          round
          placeholder="搜索"
          style="margin-bottom: 5px; width: 25vh"
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
import { getList, sendData } from '@renderer/utils/fetchUtils'
import { RowData } from 'naive-ui/es/data-table/src/interface'
import { reactive, ref, watch } from 'vue'
import { useMessage } from 'naive-ui'
import { Search } from '@vicons/ionicons5'

const message = useMessage()

const music: any = reactive({
  // 音乐列表
  systemMusic: [], // 原版音乐
  myImport: [], // 导入的音乐
  myTranslate: [], // 扒谱的音乐
  myFavorite: []
})
const nowPlayMusic = ref('没有歌曲') // 当前选中歌曲
let nowType = 'systemMusic'
const searchText = ref('')
const musicColumns = [
  {
    title: '歌名',
    key: 'name'
  }
] // 音乐列

const systemMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name
    }
  }
}
const myImportMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name
    }
  }
}
const myTranslateMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name
    }
  }
}

function handleUpdateValue(value: string) {
  searchText.value = ''
  getListData(value)
}

function handleBeforeLeave(name: string) {
  nowType = name
  return true
}

const myFavoriteMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name
    }
  }
}

watch(searchText, () => {
  getListData('systemMusic')
  getListData('myImport')
  getListData('myTranslate')
  getListData('myFavorite')
})

function followTutorial() {
  if (nowPlayMusic.value === '没有歌曲') {
    message.error('选个歌再跟弹吧靓仔')
    return
  } else {
    sendData('followSheet', {
      fileName: nowPlayMusic.value,
      type: nowType
    }).then(() => {
      window.api.open_tutorial("keyboard")
    })
  }
}
handleUpdateValue('systemMusic')

function getListData(value) {
  getList(value, searchText.value).then((_res) => {
    eval('music.' + value + '=_res')
  })
}
</script>
