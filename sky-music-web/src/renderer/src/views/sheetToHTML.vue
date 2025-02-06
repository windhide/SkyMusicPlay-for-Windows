<template>
  <n-flex align="center">
    <n-gradient-text :size="20" type="success" style="width: 100%;color:#F2E8C4">
      {{ '当前: ' + nowPlayMusic + '' }}
    </n-gradient-text>
    <n-button type="primary" ghost :loading="processFlag" @click="transfer" color="#F2E8C4"> 开始转换(自动保存在桌面) </n-button>
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
          :virtual-scroll="music.systemMusic?.length > 7"
          :row-props="selectMusic"
          row-class-name="td_css"
        />
      </n-tab-pane>
      <n-tab-pane name="myImport" tab="导入歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.myImport"
          :bordered="false"
          :min-row-height="48"
          :max-height="300"
          :virtual-scroll="music.myImport?.length > 7"
          :row-props="selectMusic"
          row-class-name="td_css"
        />
      </n-tab-pane>
      <n-tab-pane name="myTranslate" tab="转换歌曲">
        <n-data-table
          :columns="musicColumns"
          :data="music.myTranslate"
          :bordered="false"
          :min-row-height="48"
          :max-height="300"
          :virtual-scroll="music.myTranslate?.length > 7"
          :row-props="selectMusic"
          row-class-name="td_css"
        />
      </n-tab-pane>
      <n-tab-pane name="myFavorite" tab="收藏">
        <n-data-table
          :columns="musicColumns"
          :data="music.myFavorite"
          :bordered="false"
          :min-row-height="48"
          :max-height="300"
          :virtual-scroll="music.myFavorite?.length > 7"
          :row-props="selectMusic"
          row-class-name="td_css"
        />
      </n-tab-pane>
      <template #suffix>
        <n-input v-model:value="searchText" round placeholder="搜索"
          style="top:-4px;width: 25vh; margin-left: 5px">
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

// 音乐列表
const music = reactive({
  systemMusic: [],
  myImport: [],
  myTranslate: [],
  myFavorite: []
})

// 当前选中歌曲
const nowPlayMusic = ref('没有歌曲')

// 当前音乐类型
const nowType = ref<'systemMusic' | 'myImport' | 'myTranslate' | 'myFavorite'>('systemMusic')

// 搜索文本
const searchText = ref('')

// 进程标记
const processFlag = ref(false)

// 音乐列表列定义
const musicColumns = [
  { title: '歌名', key: 'name', className: 'th_css' }
]

// 选中音乐
const selectMusic = (row: RowData) => ({
  onClick: () => {
    nowPlayMusic.value = row.name
  }
})

/**
 * 更新音乐列表数据
 */
async function handleUpdateValue(value: keyof typeof music) {
  searchText.value = '' // 清空搜索
  await getListData(value)
}

/**
 * 监听搜索框变化，仅更新当前音乐类型的列表
 */
watch(searchText, async () => {
  await getListData(nowType.value)
})

/**
 * 切换音乐类型
 */
function handleBeforeLeave(name: keyof typeof music) {
  nowType.value = name
  return true
}

/**
 * 发送扒谱转换请求
 */
async function transfer() {
  if (nowPlayMusic.value === '没有歌曲') {
    message.warning('请先选择一首歌曲')
    return
  }

  try {
    await sendData('config_operate', {
      fileName: nowPlayMusic.value,
      type: nowType.value,
      operate: 'convert_sheet'
    })
    message.success('已保存在桌面')
  } catch (error) {
    console.error('转换失败:', error)
    message.error('转换失败，请重试')
  }
}

/**
 * 获取音乐列表数据
 */
async function getListData(value: keyof typeof music) {
  try {
    const res = await getList(value, searchText.value)
    music[value] = res
  } catch (error) {
    console.error(`获取 ${value} 失败:`, error)
  }
}

// 初始化加载系统音乐
handleUpdateValue('systemMusic')
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
:deep(.n-switch--active){
  --n-rail-color-active: rgb(242,232,196)!important;
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