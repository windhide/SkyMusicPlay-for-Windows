<template>
  <n-dropdown :x="xRef" :y="yRef" :options="options" :show="showDropdownRef" :on-clickoutside="onClickoutside" @select="handleSelect" />
  <div class="midi-editor">
    <n-layout>
      <n-layout-content class="midi-content">
        <canvas ref="midiCanvas" class="midi-canvas"></canvas>
      </n-layout-content>
    </n-layout>
  </div>
    <!-- 播放控制 -->
  <n-flex justify="center">
    <n-button @click="isPlaying ? pause() : play()" quaternary circle  style="font-size: 24px" color="#F2C9C4">
      <n-icon><Pause24Filled v-if="isPlaying" /><Play24Filled v-else/></n-icon> 
    </n-button>
    <n-button @click="previousColumn" quaternary circle  style="font-size: 24px" color="#F2C9C4">
      <n-icon><ArrowPrevious24Filled /></n-icon> 
    </n-button>
    <n-button @click="nextColumn" quaternary circle  style="font-size: 24px" color="#F2C9C4"> 
      <n-icon><ArrowNext24Filled /></n-icon>
    </n-button>
    <n-button @click="insertEmptyColumn" quaternary circle  style="font-size: 24px" color="#F2C9C4">
      <n-icon><TableAdd24Filled /></n-icon> 
    </n-button>
    <n-button @click="deleteCurrentColumn" quaternary circle  style="font-size: 24px" color="#F2C9C4">
      <n-icon><TableDeleteColumn24Filled /></n-icon>  
    </n-button>
    <n-button @click="playNowColumn" quaternary circle  style="font-size: 24px" color="#F2C9C4">
      <n-icon><MusicNote120Filled /></n-icon>  
    </n-button>
    <n-button @click="saveSheet" quaternary circle  style="font-size: 24px" color="#F2C9C4">
      <n-icon><Save20Filled /></n-icon>  
    </n-button>
  </n-flex>
  <n-slider v-model:value="progress" :step="1" @update:value="updateProgress" :min="1" :max="notes.length"  style="margin-bottom: 8px;" />
  <n-flex v-for="(row, index) in keys" :key="index" justify="center">
    <div v-for="(item, idx) in row" :key="idx">
      <n-button  color="#F2C9C4" style="height:75px; width: 75px;" :dashed="!item.active" @contextmenu="handleContextMenu">
        <template #icon>
          <n-icon v-if="item.type === 'cr'" :size="65" :component="cr" />
          <n-icon v-if="item.type === 'dm'" :size="65" :component="dm" />
          <n-icon v-if="item.type === 'dmcr'" :size="65" :component="dmcr" />
        </template>
      </n-button>
    </div>
    <div style="flex-basis: 100%;" />
  </n-flex>
  <div style="margin-left: 920px; margin-top: -248px; width: 415px; height: 200px;">
    <n-flex>
      <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        长按间隔（秒）
      </n-gradient-text>
      <n-input-number style="flex-basis: 40%; margin-left: 29px;" :step="0.01"/>
      <div style="flex-basis: 100%;" />
      <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        当列等待时间（秒）
      </n-gradient-text>
      <n-input-number style="flex-basis: 40%;" :step="0.01" />
      <div style="flex-basis: 100%;" />
      <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        按键激活
      </n-gradient-text>
      <n-switch :round="false" :rail-style="railStyle"  style="flex-basis: 43%;"/>
    </n-flex>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, nextTick, CSSProperties } from "vue";
import cr from "../component/svg/cr.vue"
import dm from "../component/svg/dm.vue"
import dmcr from "../component/svg/dmcr.vue"
import {
  ArrowPrevious24Filled,
  Pause24Filled,
  Play24Filled,
  ArrowNext24Filled,
  TableDeleteColumn24Filled,
  TableAdd24Filled,
  MusicNote120Filled,
  Save20Filled
} from '@vicons/fluent'

const midiCanvas = ref(null);
const isPlaying = ref(false)
const showDropdownRef = ref(false)
const xRef = ref(0)
const yRef = ref(0)
const options=[ { label: '修改长按间隔', key: 'druation'}]
function handleContextMenu(e: MouseEvent){ e.preventDefault(); showDropdownRef.value=false; nextTick().then(()=>{ showDropdownRef.value=true; xRef.value=e.clientX; yRef.value=e.clientY;})}
function onClickoutside(){ showDropdownRef.value=false;}
function railStyle({ focused, checked}){ const style: CSSProperties={}; if (checked){ style.background='#F2C9C4'; if (focused){ style.boxShadow='0 0 0 2px #F2C9C440';}} return style;}
function handleSelect(key: string | number) {
  showDropdownRef.value = false
}
const notes = ref([
  // 示例：每列激活的格子位置（1-15）
  [3, 7, 12], // 第一列激活的格子
  [1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15], // 第一列激活的格子
  [1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15], // 第一列激活的格子
]);

const keys = ref([
  [
    {key: "0", type:"dmcr", druation:"0", active: false},
    {key: "1", type:"dm", druation:"0", active: true},
    {key: "2", type:"cr", druation:"0", active: true},
    {key: "3", type:"dm", druation:"0", active: true},
    {key: "4", type:"cr", druation:"0", active: true},
  ],
  [
    {key: "5", type:"cr", druation:"0", active: true},
    {key: "6", type:"dm", druation:"0", active: true},
    {key: "7", type:"dmcr", druation:"0", active: true},
    {key: "8", type:"dm", druation:"0", active: true},
    {key: "9", type:"cr", druation:"0", active: true},
  ],
  [
    {key: "10", type:"cr", druation:"0", active: true},
    {key: "11", type:"dm", druation:"0", active: true},
    {key: "12", type:"cr", druation:"0", active: true},
    {key: "13", type:"dm", druation:"0", active: true},
    {key: "14", type:"dmcr", druation:"0", active: true},
  ]
])

// 自定义显示文字
const customTexts = [
  ['Do', 'Re', 'Mi', 'Fa', 'So', 'La', 'Ti', 'do', 're', 'mi', 'fa', 'so', 'la', 'ti', '♪'],
  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],
  ['Do', 'Re', 'Mi', 'Fa', 'So', 'La', 'Ti', 'do', 're', 'mi', 'fa', 'so', 'la', 'ti', '♪'],
];
const progress = ref(1);
const canvasWidth = 1200;
const canvasHeight = 300;
const gridSize = 8; // 每个小块大小
const columnSize = gridSize * 4; // 3个小块组成1大块
const cornerRadius = 5; // 圆角半径
const intervalId:any = ref(null);
const currentColumn = ref(0); // 当前列的索引

const drawCanvas = () => {
  const canvas:any = midiCanvas.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  // 计算视口偏移
  const viewportCenter = canvasWidth / 2;
  const currentX = currentColumn.value * columnSize;
  let offsetX = 0;
  
  // 当播放位置超过画布中点时，开始计算偏移量
  if (currentX > viewportCenter) {
    offsetX = viewportCenter - currentX;
  }

  // 清空画布
  ctx.clearRect(0, 0, canvasWidth, canvasHeight);
  
  // 保存当前状态
  ctx.save();
  // 应用偏移变换
  ctx.translate(offsetX, 0);

  // 画网格（小块）
  ctx.strokeStyle = "rgba(85, 85, 85, 0)";
  for (let x = 0; x < canvasWidth - offsetX; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvasHeight);
    ctx.stroke();
  }
  for (let y = 0; y < canvasHeight; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvasWidth - offsetX, y);
    ctx.stroke();
  }

  // 画主要的3块结构（每3列加粗）
  ctx.strokeStyle = "rgba(136, 136, 136, 0.7)";
  ctx.lineWidth = 2;
  for (let x = 0; x < canvasWidth - offsetX; x += columnSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvasHeight);
    ctx.stroke();
  }
  ctx.lineWidth = 1; // 还原默认线宽

  // 画 MIDI 音符
  ctx.fillStyle = "#F2C9C4";
  notes.value.forEach((column, columnIndex) => {
    column.forEach(row => {
      // 将1-15的位置转换为实际的y坐标
      const y = (row - 1) * (canvasHeight / 15);
      // x坐标根据列索引计算，增加2px偏移
      const x = columnIndex * columnSize + 1;
      // 使用圆角矩形
      const rectWidth = columnSize - 2;
      const rectHeight = canvasHeight/15 - 2;
      ctx.beginPath();
      ctx.moveTo(x + cornerRadius, y);
      ctx.lineTo(x + rectWidth - cornerRadius, y);
      ctx.quadraticCurveTo(x + rectWidth, y, x + rectWidth, y + cornerRadius);
      ctx.lineTo(x + rectWidth, y + rectHeight - cornerRadius);
      ctx.quadraticCurveTo(x + rectWidth, y + rectHeight, x + rectWidth - cornerRadius, y + rectHeight);
      ctx.lineTo(x + cornerRadius, y + rectHeight);
      ctx.quadraticCurveTo(x, y + rectHeight, x, y + rectHeight - cornerRadius);
      ctx.lineTo(x, y + cornerRadius);
      ctx.quadraticCurveTo(x, y, x + cornerRadius, y);
      ctx.fill();
      
      // 添加自定义文字标记
      ctx.fillStyle = "#000000";
      ctx.font = "12px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      if (columnIndex < customTexts.length && row - 1 < customTexts[columnIndex].length) {
        ctx.fillText(customTexts[columnIndex][row - 1], x + rectWidth/2, y + rectHeight/2);
      }
      ctx.fillStyle = "#F2C9C4";
    });
  });

  // 恢复状态以绘制固定位置的高亮
  ctx.restore();

  // 绘制当前列的高亮背景（固定在视口中心）
  ctx.fillStyle = "rgba(155, 149, 201, 0.5)";
  const highlightX = currentX > viewportCenter ? viewportCenter : currentX;
  ctx.fillRect(highlightX, 0, columnSize, canvasHeight);
};

const previousColumn = () => {
  if (currentColumn.value > 0) {
    currentColumn.value--;
    progress.value = currentColumn.value + 1;
    drawCanvas();
  }
};

const nextColumn = () => {
  if (currentColumn.value < notes.value.length - 1) {
    currentColumn.value++;
    progress.value = currentColumn.value + 1;
    drawCanvas();
  }
};

const insertEmptyColumn = () => {
  notes.value.splice(currentColumn.value, 0, []);
  // 同步插入空的文字列
  customTexts.splice(currentColumn.value, 0, ['Do', 'Re', 'Mi', 'Fa', 'So', 'La', 'Ti', 'do', 're', 'mi', 'fa', 'so', 'la', 'ti', '♪']);
  // 更新进度条最大值
  progress.value = currentColumn.value + 1;
  drawCanvas();
};

const deleteCurrentColumn = () => {
  notes.value.splice(currentColumn.value, 1);
  customTexts.splice(currentColumn.value, 1);
  if (currentColumn.value >= notes.value.length) {
    currentColumn.value = notes.value.length - 1;
  }
  progress.value = currentColumn.value + 1;
  drawCanvas();
};
const play = () => {
  if (intervalId.value) return;
  if (currentColumn.value >= notes.value.length) {
    currentColumn.value = 0;
    progress.value = 1;
  }
  isPlaying.value = true;
  intervalId.value = setInterval(() => {
    progress.value = currentColumn.value + 1;
    currentColumn.value++;
    drawCanvas();
    if (currentColumn.value >= notes.value.length) {
      clearInterval(intervalId.value);
      intervalId.value = null;
      isPlaying.value = false;
    }
  }, 30);
};

const playNowColumn = () =>{
  console.log("发送到游戏当中")
}

const saveSheet = () =>{
  console.log("保存音乐文件")
}

const pause = () => {
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = null;
    isPlaying.value = false;
  }
};

const updateProgress = () => {
  currentColumn.value = progress.value - 1;
  drawCanvas();
};

// 挂载时初始化 Canvas
onMounted(() => {
  window.api.window_size(774,1500)
  const canvas:any = midiCanvas.value;
  if (canvas) {
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    drawCanvas();
  }
});
onUnmounted(() => {
  pause(); // 组件销毁时停止动画
  window.api.window_size(0,0)
});
</script>

<style scoped>
.midi-editor {
  display: flex;
  margin-top:20px;
  height: 380px;
  overflow: hidden;
  background: transparent
}
.midi-content {
  flex-grow: 1;
  position: relative;
  background: transparent;
  padding-top: 30px;
}
.midi-canvas {
  width: 100%;
  height: 100%;
  display: block;
  background: transparent;
}
:deep(.n-layout){
  background: transparent !important;
}


:deep(.n-input){
  --n-border-hover: 1px solid rgb(242,232,196)!important;
  --n-border-focus: 1px solid rgb(242,232,196)!important;
  --n-caret-color: rgb(242,232,196)!important;
  --n-color-focus: rgba(242,232,196,0.1)!important;
}
</style>
