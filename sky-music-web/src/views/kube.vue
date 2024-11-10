<template>
  <n-flex align="center">
    <n-gradient-text :size="24" type="success" style="width: 100%;">
      转换歌曲
    </n-gradient-text>
    <n-button type="warning" ghost>
      选择文件
    </n-button>
    <n-button type="info" ghost>
      选择文件夹
    </n-button>
    <n-button type="primary" ghost>
      开始转换
    </n-button>
  </n-flex>

  <n-card style="margin-top: 20px">
    <n-tabs type="line" animated>
      <n-tab-pane name="noTranslateMusicData" tab="未转换歌曲">
        <n-data-table :columns="musicColumns" :data="music.noTranslateMusicData" :bordered="false" :max-height="330" virtual-scroll
          :row-props="musicSelect" />
      </n-tab-pane>
      <n-tab-pane name="translateData" tab="已转换歌曲">
        <n-data-table :columns="musicColumns" :data="music.translateData" :bordered="false" :max-height="300" :scroll-x="1800"
          virtual-scroll />
      </n-tab-pane>
    </n-tabs>
  </n-card>

</template>

<script lang="ts" setup>
import { getData } from '@/utils/fetchUtils'
import { RowData } from 'naive-ui/es/data-table/src/interface';
import { reactive,ref } from 'vue';
let music: any = reactive({ // 音乐列表
    translateOriginalMusic:[], // 导入的音乐
    translateData:[] // 扒谱的音乐
})
let musicColumns = [
  {
    title: '歌名',
    key: 'name'
  }
] // 音乐列

getData("").then((res: { systemMusic: any; myImport: any; myTranslate: any; }) => {
  music.translateData.push(...res.myTranslate)
  music.translateOriginalMusic.push(...res.translateOriginalMusic)
})

</script>