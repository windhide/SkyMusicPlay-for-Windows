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
    <n-upload ref="upload" action="#" :default-upload="false" accept=".txt" @change="handleUploadSheet" style="flex-basis: 1%;" :show-file-list="false">
      <n-button quaternary circle  style="font-size: 22px" color="#F2C9C4">
        <n-icon><ArrowUpload24Filled /></n-icon> 
      </n-button> 
    </n-upload>
  </n-flex>
  <n-slider v-model:value="progress" :step="1" @update:value="updateProgress" :min="1" :max="notes.length"  style="margin-bottom: 8px;" />
  <n-flex v-for="(row, index) in keys" :key="index" justify="center">
    <div v-for="(item, idx) in row" :key="idx" style="margin-top: 8px;">
      <n-button  color="#F2C9C4" style="height:75px; width: 75px;" :dashed="!item.active" @contextmenu="handleContextMenu" @click="handleButtonClick(item,index,idx)">
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
        长按间隔（秒）
      </n-gradient-text>
      <n-input-number v-model:value="downDuration" style="flex-basis: 40%; margin-left: 29px;" :step="0.01"/>
      <div style="flex-basis: 100%;" />
      <n-gradient-text  gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        列后等待延迟（秒）
      </n-gradient-text>
      <n-input-number v-model:value="columnAfterDuration" style="flex-basis: 40%;" :step="0.01" />
      <div style="flex-basis: 100%;" />
      <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        按键激活
      </n-gradient-text>
      <n-switch v-model:value="keyActive" :round="false" :rail-style="railStyle"  style="flex-basis: 43%; margin-top: 5px;"/>
      <div style="flex-basis: 100%;" />
      <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px;">
        歌曲名字
      </n-gradient-text>
      <n-input v-model:value="fileName" type="textarea" placeholder="歌曲名字/文件名字" style="flex-basis: 57%;" :autosize="{ minRows: 1, maxRows: 4 }"/>
    </n-flex>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, nextTick, CSSProperties, watch } from "vue";
import{ ArrowPrevious24Filled, Pause24Filled, Play24Filled, ArrowNext24Filled, TableDeleteColumn24Filled, TableAdd24Filled, MusicNote120Filled, Save20Filled, ArrowUpload24Filled} from '@vicons/fluent'
import cr from "../component/svg/cr.vue"
import dm from "../component/svg/dm.vue"
import dmcr from "../component/svg/dmcr.vue"
import { UploadFileInfo, useMessage } from "naive-ui";

const midiCanvas = ref(null);
const isPlaying = ref(false)
const showDropdownRef = ref(false)
const xRef = ref(0)
const yRef = ref(0)
const options=[ { label: '修改长按间隔', key: 'duration'}]
const fileName = ref("")
const columnAfterDuration = ref(0)
const downDuration = ref(0)
const keyActive = ref(false)

function handleContextMenu(e: MouseEvent){ e.preventDefault(); showDropdownRef.value=false; nextTick().then(()=>{ showDropdownRef.value=true; xRef.value=e.clientX; yRef.value=e.clientY;})}
function onClickoutside(){ showDropdownRef.value=false;}
function railStyle({ focused, checked}){ const style: CSSProperties={}; if (checked){ style.background='#F2C9C4'; if (focused){ style.boxShadow='0 0 0 2px #F2C9C440';}} return style;}
function handleSelect(key: string | number) {
  showDropdownRef.value = false
}
const notes = ref<number[][]>([]);
const keys=ref([ [ {key: "0", type:"dmcr", duration:0, active: false}, {key: "1", type:"dm", duration:0, active: false}, {key: "2", type:"cr", duration:0, active: false}, {key: "3", type:"dm", duration:0, active: false}, {key: "4", type:"cr", duration:0, active: false}, ], [ {key: "5", type:"cr", duration:0, active: false}, {key: "6", type:"dm", duration:0, active: false}, {key: "7", type:"dmcr", duration:0, active: false}, {key: "8", type:"dm", duration:0, active: false}, {key: "9", type:"cr", duration:0, active: false}, ], [ {key: "10", type:"cr", duration:0, active: false}, {key: "11", type:"dm", duration:0, active: false}, {key: "12", type:"cr", duration:0, active: false}, {key: "13", type:"dm", duration:0, active: false}, {key: "14", type:"dmcr", duration:0, active: false}, ]
])
// 自定义显示文字
const durationNotes = ref<string[][]>([]);
const progress = ref(1);
const canvasWidth = 1200;
const canvasHeight = 300;
const gridSize = 8; // 每个小块大小
const columnSize = gridSize * 4; // 3个小块组成1大块
const cornerRadius = 5; // 圆角半径
const intervalId:any = ref(null);
const currentColumn = ref(0); // 当前列的索引
const message = useMessage()

const drawCanvas=()=>{ const canvas:any=midiCanvas.value; if (!canvas) return; const ctx=canvas.getContext("2d"); const viewportCenter=canvasWidth / 2; const currentX=currentColumn.value * columnSize; let offsetX=0; if (currentX >viewportCenter){ offsetX=viewportCenter - currentX;} ctx.clearRect(0, 0, canvasWidth, canvasHeight); ctx.save(); ctx.translate(offsetX, 0); ctx.strokeStyle="rgba(85, 85, 85, 0)"; for (let x=0; x < canvasWidth - offsetX; x +=gridSize){ ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvasHeight); ctx.stroke();} for (let y=0; y < canvasHeight; y +=gridSize){ ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvasWidth - offsetX, y); ctx.stroke();} ctx.strokeStyle="rgba(136, 136, 136, 0.7)"; ctx.lineWidth=2; for (let x=0; x < canvasWidth - offsetX; x +=columnSize){ ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvasHeight); ctx.stroke();} ctx.lineWidth=1; ctx.fillStyle="#F2C9C4"; notes.value.forEach((column, columnIndex)=>{ column.forEach(row=>{ const y=(row - 1) * (canvasHeight / 15); const x=columnIndex * columnSize + 1; const rectWidth=columnSize - 2; const rectHeight=canvasHeight/15 - 2; ctx.beginPath(); ctx.moveTo(x + cornerRadius, y); ctx.lineTo(x + rectWidth - cornerRadius, y); ctx.quadraticCurveTo(x + rectWidth, y, x + rectWidth, y + cornerRadius); ctx.lineTo(x + rectWidth, y + rectHeight - cornerRadius); ctx.quadraticCurveTo(x + rectWidth, y + rectHeight, x + rectWidth - cornerRadius, y + rectHeight); ctx.lineTo(x + cornerRadius, y + rectHeight); ctx.quadraticCurveTo(x, y + rectHeight, x, y + rectHeight - cornerRadius); ctx.lineTo(x, y + cornerRadius); ctx.quadraticCurveTo(x, y, x + cornerRadius, y); ctx.fill(); ctx.fillStyle="#000000"; ctx.font="12px Arial"; ctx.textAlign="center"; ctx.textBaseline="middle"; if (columnIndex < durationNotes.value.length && row - 1 < durationNotes.value[columnIndex].length){ ctx.fillText(durationNotes.value[columnIndex][row - 1], x + rectWidth/2, y + rectHeight/2);} ctx.fillStyle="#F2C9C4";});}); ctx.restore(); ctx.fillStyle="rgba(155, 149, 201, 0.5)"; const highlightX=currentX >viewportCenter ? viewportCenter : currentX; ctx.fillRect(highlightX, 0, columnSize, canvasHeight);};

const previousColumn=()=>{ if (currentColumn.value >0){ currentColumn.value--; progress.value=currentColumn.value + 1; drawCanvas();}};
const nextColumn=()=>{ if (currentColumn.value < notes.value.length - 1){ currentColumn.value++; progress.value=currentColumn.value + 1; drawCanvas();}};
const playNowColumn = () =>{
  console.log("发送到游戏当中")
}
const saveSheet = () =>{
  console.log("保存音乐文件")
  console.log(notes.value)
  console.log(durationNotes.value)
  saveFile(fileName.value,"")
}

const saveFile=(filename, content)=>{ const blob=new Blob([content],{ type: "text/plain"}); const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=filename; document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(a.href);}
function handleUploadSheet(options:{ file: any; fileList: UploadFileInfo[]}) {
  window.api.readFile(options?.file?.file?.path, true).then((res:any) => {
    if (res != false) {
      message.success("谱子加载成功")
      fileName.value = res[0]["name"]
      let song_notes = res[0]["songNotes"]
      let result = precessSongNotes(song_notes)
      notes.value = []
      durationNotes.value = []
      result.forEach(element => {
      let durationNote = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
      notes.value.push(element.key.replace("Key", "").split("Key").map(part=>{ 
        durationNote[part] = element.duration
        return parseInt(part, 10)+1
      }))
      durationNotes.value.push(durationNote)
      });
    } else {
      message.error("谱子加载失败")
    }
    drawCanvas()
  })
}

const precessSongNotes=(song_notes:any)=>{ let result:any=[]; let combined_time=-1; let combined_keys=''; for (let i=0; i < song_notes.length; i++){ let note=song_notes[i]; let current_time=note.time; let key=note.key; let duration=note?.duration || 0; if (current_time !==combined_time){ if (combined_keys){ let next_time=(i < song_notes.length - 1) ? song_notes[i + 1].time : current_time; let delay=next_time - combined_time; result.push({ key: combined_keys, delay, duration});} combined_time=current_time; combined_keys=key.match(/(Key-?\d+)/)[0];} else{ combined_keys +=key.match(/(Key-?\d+)/)[0];}} if (combined_keys){ result.push({ key: combined_keys, delay: 0, duration: 0});} return result}
const play=()=>{ if (intervalId.value) return; if (currentColumn.value >=notes.value.length){ currentColumn.value=0; progress.value=1;} isPlaying.value=true; intervalId.value=setInterval(()=>{ progress.value=currentColumn.value + 1; currentColumn.value++; drawCanvas(); if (currentColumn.value >=notes.value.length){ clearInterval(intervalId.value); intervalId.value=null; isPlaying.value=false;}}, 30);};
const pause=()=>{ if (intervalId.value){ clearInterval(intervalId.value); intervalId.value=null; isPlaying.value=false;}};
const deleteCurrentColumn=()=>{ notes.value.splice(currentColumn.value, 1); durationNotes.value.splice(currentColumn.value, 1); if (currentColumn.value >=notes.value.length){ currentColumn.value=notes.value.length - 1;} progress.value=currentColumn.value + 1; drawCanvas();};
const insertEmptyColumn=()=>{ notes.value.splice(currentColumn.value, 0, []); durationNotes.value.splice(currentColumn.value, 0, ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']); progress.value=currentColumn.value + 1; drawCanvas();};
const updateProgress=()=>{ currentColumn.value=progress.value - 1; drawCanvas();};
watch(progress, syncCanvasToKeysArea)
function syncCanvasToKeysArea() {
  keys.value=[ ["dmcr", "dm", "cr", "dm", "cr"], ["cr", "dm", "dmcr", "dm", "cr"], ["cr", "dm", "cr", "dm", "dmcr"] ].map((row, rowIndex)=>row.map((type, colIndex)=>({ key: String(rowIndex * 5 + colIndex), type, duration: 0, active: false})) );
  if (notes.value.length == 0) return;
  notes.value[progress.value - 1].forEach(res => {
    if (res >= 1 && res <= 15) {
      let row = Math.floor((res - 1) / 5);
      let col = (res - 1) % 5;
      keys.value[row][col].active = true;
    }
  });
}
function handleButtonClick(item, column, row) {
  const index = row + column * 5;
  const progressIndex = progress.value - 1;
  item.active = !item.active;
  if (item.active) {
    console.log(index + 1);
    notes.value[progressIndex].push(index + 1);
    durationNotes.value[progressIndex][index] = item.duration ? String(item.duration) : "";
  } else {
    notes.value[progressIndex] = notes.value[progressIndex].filter(res => res !== index + 1);
    durationNotes.value[progressIndex][index] = "";
  }
  syncKeysAreaToCanvas();
}

function syncKeysAreaToCanvas(){
  drawCanvas()
}

onMounted(()=>{ window.api.window_size(774,1500); const canvas:any=midiCanvas.value; if (canvas){ canvas.width=canvasWidth; canvas.height=canvasHeight; drawCanvas(); syncCanvasToKeysArea();}});
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
