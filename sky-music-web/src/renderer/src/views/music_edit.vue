<template>
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
    <n-button @click="previousColumn" quaternary circle style="font-size: 24px" color="#F2C9C4">
      <n-icon><ArrowPrevious24Filled /></n-icon> 
    </n-button>
    <n-button @click="nextColumn" quaternary circle style="font-size: 24px" color="#F2C9C4"> 
      <n-icon><ArrowNext24Filled /></n-icon>
    </n-button>
    <n-button @click="insertEmptyColumn" quaternary circle style="font-size: 24px" color="#F2C9C4">
      <n-icon><TableAdd24Filled /></n-icon> 
    </n-button>
    <n-button @click="deleteCurrentColumn" quaternary circle style="font-size: 24px" color="#F2C9C4">
      <n-icon><TableDeleteColumn24Filled /></n-icon>  
    </n-button>
    <n-button @click="playNowColumn" quaternary circle style="font-size: 24px" color="#F2C9C4">
      <n-icon><MusicNote120Filled /></n-icon>  
    </n-button>
    <n-button @click="saveSheet" quaternary circle style="font-size: 24px" color="#F2C9C4">
      <n-icon><Save20Filled /></n-icon>  
    </n-button>
    <n-button @click="isPlaying ? pause() : reverse()" quaternary circle  style="font-size: 24px; transform: rotate(180deg);" color="#F2C9C4">
      <n-icon><Pause24Filled v-if="isPlaying" /><Play24Filled v-else/></n-icon> 
    </n-button>
    <n-upload ref="upload" action="#" :default-upload="false" accept=".txt" @change="handleUploadSheet" style="flex-basis: 1%;" :show-file-list="false">
      <n-button quaternary circle  style="font-size: 22px" color="#F2C9C4">
        <n-icon><ArrowUpload24Filled /></n-icon> 
      </n-button> 
    </n-upload>
  </n-flex>
  <n-slider v-model:value="progress" :step="1" @update:value="updateProgress" :min="1" :max="notes.length"  style="margin-bottom: 8px;" />
  <n-flex v-for="(row, index) in keys" :key="index" justify="center">
    <div v-for="(item, idx) in row" :key="idx" style="margin-top: 8px;">
      <n-button  color="#F2C9C4" style="height:75px; width: 75px;" :dashed="!item.active" @click="handleButtonClick(item,index,idx)">
        <template #icon>
          <n-icon v-if="item.type === 'cr'" :size="65" :component="cr" />
          <n-icon v-if="item.type === 'dm'" :size="65" :component="dm" />
          <n-icon v-if="item.type === 'dmcr'" :size="65" :component="dmcr" />
        </template>
      </n-button>
    </div>
    <div style="flex-basis: 100%;" />
  </n-flex>
  <div style="margin-left: 920px; margin-top: -260px; width: 415px; height: 200px;">
    <n-flex>
      <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        当列长按间隔（ms）
      </n-gradient-text>
      <n-input-number v-model:value="columnDownDuration" style="flex-basis: 40%;" :step="10" :min="0" />
      <div style="flex-basis: 100%;" />
      <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        列后等待延迟（ms）
      </n-gradient-text>
      <n-input-number v-model:value="columnAfterDuration" style="flex-basis: 40%;" :step="10" :min="0" />
      <div style="flex-basis: 100%;" />
      <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        歌曲名字
      </n-gradient-text>
      <n-input v-model:value="fileName" type="textarea" placeholder="歌曲名字/文件名字" style="flex-basis: 58%;" :autosize="{ minRows: 1, maxRows: 4 }"/>
    </n-flex>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, nextTick, CSSProperties, watch } from "vue";
import{ ArrowPrevious24Filled, Pause24Filled, Play24Filled, ArrowNext24Filled, TableDeleteColumn24Filled, TableAdd24Filled, MusicNote120Filled, Save20Filled, ArrowUpload24Filled, CommunicationPerson20Filled} from '@vicons/fluent'
import cr from "../component/svg/cr.vue"
import dm from "../component/svg/dm.vue"
import dmcr from "../component/svg/dmcr.vue"
import { UploadFileInfo, useMessage } from "naive-ui";
import { sendData } from "@renderer/utils/fetchUtils";

const midiCanvas = ref(null);
const isPlaying = ref(false)
const fileName = ref("")
const columnAfterDuration = ref(0)
const columnDownDuration = ref(0)
const nowButton = ref(-1)

const keys=ref([ [ {key: "0", type:"dmcr", duration:0, active: false}, {key: "1", type:"dm", duration:0, active: false}, {key: "2", type:"cr", duration:0, active: false}, {key: "3", type:"dm", duration:0, active: false}, {key: "4", type:"cr", duration:0, active: false}, ], [ {key: "5", type:"cr", duration:0, active: false}, {key: "6", type:"dm", duration:0, active: false}, {key: "7", type:"dmcr", duration:0, active: false}, {key: "8", type:"dm", duration:0, active: false}, {key: "9", type:"cr", duration:0, active: false}, ], [ {key: "10", type:"cr", duration:0, active: false}, {key: "11", type:"dm", duration:0, active: false}, {key: "12", type:"cr", duration:0, active: false}, {key: "13", type:"dm", duration:0, active: false}, {key: "14", type:"dmcr", duration:0, active: false}, ]
])
// 自定义显示文字
const durationNotes = ref<number[]>([0]); // 长按表
const notes = ref<number[][]>([[]]); // 谱表
const timeNotes = ref<number[]>([10]); // 延迟表
const progress = ref(1);
const canvasWidth = 1200;
const canvasHeight = 300;
const gridSize = 8; // 每个小块大小
const columnSize = gridSize * 4; // 3个小块组成1大块
const cornerRadius = 5; // 圆角半径
const intervalId:any = ref(null);
const currentColumn = ref(0); // 当前列的索引
const message = useMessage()

const drawCanvas = () => {
  const canvas: any = midiCanvas.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const viewportCenter = canvasWidth / 2;
  const currentX = currentColumn.value * columnSize;
  let offsetX = 0;
  if (currentX > viewportCenter) {
    offsetX = viewportCenter - currentX;
  }
  ctx.clearRect(0, 0, canvasWidth, canvasHeight);
  ctx.save();
  ctx.translate(offsetX, 0);
  ctx.strokeStyle = "rgba(85, 85, 85, 0)";
  
  // 绘制网格
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
  
  // 绘制列线
  ctx.strokeStyle = "rgba(136, 136, 136, 0.7)";
  ctx.lineWidth = 2;
  for (let x = 0; x < canvasWidth - offsetX; x += columnSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvasHeight);
    ctx.stroke();
  }
  
  ctx.lineWidth = 1;
  ctx.fillStyle = "#F2C9C4";
  
  // 绘制音符
  notes.value.forEach((column, columnIndex) => {
    column.forEach(row => {
      const y = (row - 1) * (canvasHeight / 15);
      const x = columnIndex * columnSize + 1;
      const rectWidth = columnSize - 2;
      const rectHeight = canvasHeight / 15 - 2;
      
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
      
      ctx.fillStyle = "#000000";
      ctx.font = "12px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      // 计算当前列应该显示的 durationNotes
      let textToDisplay = "";
      if (durationNotes.value.length === 1) {
        // 只有一个值，应用到所有这一列的格子
        textToDisplay = String(durationNotes.value[0]);  // 确保 0 也能正确显示
      } else if (columnIndex < durationNotes.value.length) {
        // 多个值时，按列索引显示
        textToDisplay = String(durationNotes.value[columnIndex]);
      }

      // 在当前列的所有音符上显示相应的 durationNotes 值
      ctx.fillText(textToDisplay, x + rectWidth / 2, y + rectHeight / 2);

      ctx.fillStyle = "#F2C9C4";
    });
  });
  
  ctx.restore();
  
  // 高亮当前列
  ctx.fillStyle = "rgba(155, 149, 201, 0.5)";
  const highlightX = currentX > viewportCenter ? viewportCenter : currentX;
  ctx.fillRect(highlightX, 0, columnSize, canvasHeight);
};

const previousColumn=()=>{ if (currentColumn.value >0){ currentColumn.value--; progress.value=currentColumn.value + 1; drawCanvas();playNowColumn();}};
const nextColumn=()=>{ if (currentColumn.value < notes.value.length - 1){ currentColumn.value++; progress.value=currentColumn.value + 1; drawCanvas();playNowColumn();}};
const playNowColumn = () => {
  const progressIndex = progress.value - 1;
  const currentNotes = notes.value[progressIndex];
  const noteCount = currentNotes.length;
  const time = timeNotes.value[progressIndex];
  const songNote = currentNotes.map(element => ({
    time: Number(time),
    key: `${noteCount}Key${element - 1}`,
    duration: Number(durationNotes.value[progressIndex]) || 0
  }));
  sendData("play_operate",{
    operate: 'start',
    sheet:songNote
  })
  return Number(time)
};
const saveSheet = () =>{
  const templateMusicFormat = [
    {
        "name": fileName.value,
        "author": "edit by SkyMusic",
        "transcribedBy": "WindHide's Music SoftWare",
        "bpm": 0,
        "bitsPerPage": 15,
        "pitchLevel": 0,
        "isComposed": true,
        "songNotes": getSheetToMemory(0),
        "isEncrypted": false,
    }
  ]
  saveFile(fileName.value,JSON.stringify(templateMusicFormat))
}

const saveFile=(filename, content)=>{ const blob=new Blob([content],{ type: "text/plain"}); const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=filename; document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(a.href);}
async function handleUploadSheet(options: { file: any; fileList: UploadFileInfo[] }) {
  try {
    const res = await window.api.readFile(options.file.file.path, true);
    if (!res) {
      message.error("谱子加载失败");
      return;
    }
    message.success("谱子加载成功");
    fileName.value = res[0]?.name || "未知文件";
    const songNotes = res[0]?.songNotes || [];
    notes.value = [];
    durationNotes.value = [];
    timeNotes.value = [];
    let groupDemo:any = Object.values(
        songNotes.reduce((acc, note) => {
            if (!acc[note.time]) {
                acc[note.time] = { time: note.time, keys: [], duration:note.duration || 0 };
            }
            acc[note.time].keys.push(note.key);
            return acc;
        }, {})
    )
    groupDemo.forEach((item:any,index)=>{
        let note:any = []
        item.keys.forEach(key => {
          note.push(Number(key.match(/(Key-?\d+)/)[0].replace("Key","")) + 1);
        });
        notes.value.push(note)
        durationNotes.value.push(item.duration)
        timeNotes.value.push(groupDemo[index + 1] ? groupDemo[index + 1].time - item.time : 0)
    })
    syncCanvasToKeysArea()
    drawCanvas()
    currentColumn.value = 0;
    progress.value = 1;
  } catch (error) {
    message.error("谱子加载失败");
    console.error(error);
  }
  console.log(notes.value,durationNotes.value,timeNotes.value)
}
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let isFirst = true
const play = async () => { 
  if (intervalId.value) return; // 避免重复启动
  if (currentColumn.value >= notes.value.length) {
    currentColumn.value = 0; 
    progress.value = 1;
  } 
  isPlaying.value = true; 
  intervalId.value = true; 
  let inWhileColumn = currentColumn.value
  while (inWhileColumn < notes.value.length && intervalId.value) {
    inWhileColumn++; 
    if (isFirst){
      playNowColumn()
      isFirst = false;
    }else{
      nextColumn()
    }
    await sleep(timeNotes.value[progress.value - 1]);
    const end = performance.now();
  }
  intervalId.value = null;
  isPlaying.value = false;
  isFirst = true;
};
const pause = () => { 
  intervalId.value = null; // 结束 while 循环
  isPlaying.value = false;
  isFirst = false;
};
const reverse = async () => { 
  if (intervalId.value) return; // 避免重复启动

  if (currentColumn.value >= notes.value.length) {
    currentColumn.value = 0; 
    progress.value = 1;
  } 
  isPlaying.value = true; 
  intervalId.value = true; 
  let inWhileColumn = currentColumn.value
  while (inWhileColumn >= 0 && intervalId.value) {
    inWhileColumn--; 
    if (isFirst){
      playNowColumn()
      isFirst = false;
    }else{
      previousColumn()
    }
    await sleep(timeNotes.value[progress.value - 2]);
  }
  intervalId.value = null;
  isPlaying.value = false;
  isFirst = true;
};
const deleteCurrentColumn=()=>{ notes.value.splice(currentColumn.value, 1); durationNotes.value.splice(currentColumn.value, 0); if (currentColumn.value >=notes.value.length){ currentColumn.value=notes.value.length - 1;} progress.value=currentColumn.value + 1; drawCanvas();};
const insertEmptyColumn = () => {
  const insertIndex = currentColumn.value + 1; // 计算插入位置
  notes.value.splice(insertIndex, 0, []); // 在光标后插入空列
  durationNotes.value.splice(insertIndex, 0, 0); // 插入默认时长 0
  timeNotes.value.splice(insertIndex, 0, 0); // 插入默认时间差 0
  progress.value = insertIndex + 1; // 更新进度
  drawCanvas(); // 重新绘制
  console.log(notes.value,durationNotes.value,timeNotes.value)
};const updateProgress=()=>{ currentColumn.value=progress.value - 1; drawCanvas();};
watch(progress, syncCanvasToKeysArea)
watch(columnAfterDuration, (newValue, _oldValue) => {
  if (columnDownDuration.value >= newValue) {
    message.info("长按间隔需要小于列后等待延迟，已自动调整");
    columnDownDuration.value = Math.max(newValue - 10, 0);
  }
  const finalValue = Math.max(newValue, 10);
  columnAfterDuration.value = finalValue;
  timeNotes.value[progress.value - 1] = finalValue;
  drawCanvas();
});
watch(columnDownDuration, (newValue, _oldValue) => {
  if (newValue >= columnAfterDuration.value) {
    message.info("长按间隔需要小于等待间隔，已自动增加列后等待延迟");
    columnAfterDuration.value = newValue + 10;
  }
  durationNotes.value[progress.value - 1] = newValue;
  drawCanvas();
});
watch(nowButton, ()=>{
  columnDownDuration.value = Number(durationNotes.value[progress.value -1])
})
function syncCanvasToKeysArea() {
  keys.value=[ ["dmcr", "dm", "cr", "dm", "cr"], ["cr", "dm", "dmcr", "dm", "cr"], ["cr", "dm", "cr", "dm", "dmcr"] ].map((row, rowIndex)=>row.map((type, colIndex)=>({ key: String(rowIndex * 5 + colIndex), type, duration: 0, active: false})) );
  if (notes.value.length == 0) return;
  notes.value[progress.value - 1]?.forEach(res => {
    if (res >= 1 && res <= 15) {
      let row = Math.floor((res - 1) / 5);
      let col = (res - 1) % 5;
      keys.value[row][col].active = true;
    }
  });
  columnDownDuration.value = durationNotes.value[progress.value - 1]
  columnAfterDuration.value = timeNotes.value[progress.value - 1]
  drawCanvas()
}
function handleButtonClick(item, column, row) {
  const index = row + column * 5;
  const progressIndex = progress.value - 1;
  item.active = !item.active;
  if (item.active) {
    notes.value[progressIndex].push(index + 1);
    durationNotes.value[progressIndex] = item.duration ? item.duration : 0;
  } else {
    notes.value[progressIndex] = notes.value[progressIndex].filter(res => res !== index + 1);
    durationNotes.value[progressIndex] = 0;
  }
  drawCanvas()
  nowButton.value = column * 5 + row
}

function getSheetToMemory(startIdx) {
  let demoSongNotes: any = [];
  let sumTimestamp = 0;
  for (let index = startIdx; index < notes.value.length; index++) {
    for (let j = 0; j < notes.value[index].length; j++) {
      let row = notes.value[index][j];
      demoSongNotes.push({
        time: sumTimestamp,
        key: `${notes.value[index].length}Key${row - 1}`,
        duration: Number(durationNotes.value[index]) || 0
      });
    }
    sumTimestamp += timeNotes.value[index];
  }
  return demoSongNotes
}

onMounted(()=>{ window.api.window_size(774,1500); const canvas:any=midiCanvas.value; if (canvas){ canvas.width=canvasWidth; canvas.height=canvasHeight; drawCanvas()}});
onUnmounted(()=>{ pause(); window.api.window_size(0,0);});
</script>

<style scoped>
.midi-editor {
  display: flex;
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
