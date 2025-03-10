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
    <n-button @click="musicActive = true" quaternary circle style="font-size: 24px" color="#F2C9C4">
      <n-icon><AppsListDetail24Filled /></n-icon>  
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
        当列乐谱总时长：
      </n-gradient-text>
      <n-gradient-text gradient="linear-gradient(90deg, rgb(242,201,196), rgb(221,242,196))" style="margin-top: 5px; margin-left: 21px;">
        {{ 
          (() => {
            const totalMilliseconds = timeNotes.reduce((acc, currentValue) => acc + currentValue, 0);
            const minutes = Math.floor(totalMilliseconds / 60000);  // 60000毫秒 = 1分钟
            const seconds = Math.floor((totalMilliseconds % 60000) / 1000);  // 剩余的秒数
            return `${minutes}分 ${seconds}秒`;
          })()
        }}      </n-gradient-text>
      <div style="flex-basis: 100%;" />
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
    <n-drawer
      v-model:show="musicActive"
      :width="900"
      placement="left"
      :trap-focus="false"
      :block-scroll="false"
    >
    <n-drawer-content>
      <n-card style="margin-left: -16px; width: 860px;" :bordered="false">
        <n-tabs type="bar" animated size="small" @update:value="handleUpdateValue" @before-leave="handleBeforeLeave" :value="tabsNumber">
          <n-tab-pane name="systemMusic" tab="自带歌曲">
            <n-data-table :columns="tableColumns" :data="music.systemMusic" :bordered="false" :min-row-height="48" ref="systemMusic"
              :max-height="600" :virtual-scroll="music.systemMusic?.length > 7" :row-class-name="rowClassName" 
              style="
                --n-td-color: rgba(57, 57, 62, 0);
                --n-th-color-hover: rgba(57, 57, 62, 0);
                --n-th-color: rgba(57, 57, 62, 0);
                --n-td-color-hover: rgba(0, 0, 0, 0.2);
              "/>
          </n-tab-pane>
          <n-tab-pane name="myImport" tab="导入歌曲" ref="myImport">
            <n-data-table :columns="tableColumns" :data="music.myImport" :bordered="false" :min-row-height="48" ref="myImport"
            :max-height="600" :virtual-scroll="music.myImport?.length > 7"  :row-class-name="rowClassName"
            style="
                --n-td-color: rgba(57, 57, 62, 0);
                --n-th-color-hover: rgba(57, 57, 62, 0);
                --n-th-color: rgba(57, 57, 62, 0);
                --n-td-color-hover: rgba(0, 0, 0, 0.2);
              "/>
          </n-tab-pane>
          <n-tab-pane name="myTranslate" tab="转换歌曲" ref="myTranslate">
            <n-data-table :columns="tableColumns" :data="music.myTranslate" :bordered="false" :min-row-height="48" ref="myTranslate"
            :max-height="600" :virtual-scroll="music.myTranslate?.length > 7" :row-class-name="rowClassName" 
            style="
                --n-td-color: rgba(57, 57, 62, 0);
                --n-th-color-hover: rgba(57, 57, 62, 0);
                --n-th-color: rgba(57, 57, 62, 0);
                --n-td-color-hover: rgba(0, 0, 0, 0.2);
              "/>
          </n-tab-pane>
          <n-tab-pane name="myFavorite" tab="收藏" ref="myFavorite">
            <n-data-table :columns="tableColumns" :data="music.myFavorite" :bordered="false" :min-row-height="48" ref="myFavorite"
            :max-height="600" :virtual-scroll="music.myFavorite?.length > 7"  :row-class-name="rowClassName"
            style="
                --n-td-color: rgba(57, 57, 62, 0);
                --n-th-color-hover: rgba(57, 57, 62, 0);
                --n-th-color: rgba(57, 57, 62, 0);
                --n-td-color-hover: rgba(0, 0, 0, 0.2);
              "/>
          </n-tab-pane>
          <template #suffix>
            <n-input v-model:value="searchText" round placeholder="搜索"
              style="top:-3px;width: 25vh; margin-left: 5px">
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

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, nextTick, CSSProperties, watch, reactive, h } from "vue";
import{ ArrowPrevious24Filled, Pause24Filled, Play24Filled, ArrowNext24Filled, TableDeleteColumn24Filled, TableAdd24Filled, MusicNote120Filled, Save20Filled, ArrowUpload24Filled, AppsListDetail24Filled} from '@vicons/fluent'
import{ Search} from '@vicons/ionicons5'
import cr from "../component/svg/cr.vue"
import dm from "../component/svg/dm.vue"
import dmcr from "../component/svg/dmcr.vue"
import { NButton, UploadFileInfo, useDialog, useMessage } from "naive-ui";
import { getList, sendData } from "@renderer/utils/fetchUtils";
import { RowData } from "naive-ui/es/data-table/src/interface";
import { debounce } from "lodash-es";
import { onBeforeRouteLeave } from "vue-router";

const midiCanvas = ref(null);
const isPlaying = ref(false)
const musicActive = ref(false)
const fileName = ref("")
const searchText = ref('')
const columnAfterDuration = ref(0)
const columnDownDuration = ref(0)
const nowButton = ref(-1)
const tableColumns=[ { title: '歌名', key: 'name', resizable: true, className: 'th_css', ellipsis:{ tooltip: true}}, { title: '操作', key: 'operation', width: 60, className: 'th_css', render(row){ return h( NButton, { size: 'medium', text: true, onClick: ()=>{ pause();sendData("path",{ "type":nowType}).then(res=>{ loadFile(`${res}\\${row.name}.txt`).then(()=>{ musicActive.value=false;})})}}, { default: ()=>{ return '👈'}} )}}
]
let nowType = 'systemMusic'
const fetchListData = debounce(() => {
  getListData('myFavorite');
  getListData('systemMusic');
  getListData('myImport');
  getListData('myTranslate');
}, 200);
watch(searchText, fetchListData)
function rowClassName(row: RowData) {
  if (row?.position) {
    return 'table_position'
  }
  return 'td_css'
}
// 处理抽屉切换前动作
function handleBeforeLeave(name: string) {
  nowType = name
  return true
}
const tabsNumber = ref("systemMusic")
function handleUpdateValue(value: string) {
  tabsNumber.value = value
  getListData(value)
}
async function getListData(value) {
  await getList(value, searchText.value).then((_res) => {
    eval('music.' + value + '=_res')
  })
}
const music: any=reactive({ systemMusic: [], myImport: [], myTranslate: [], myFavorite: [], musicList: []})
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
const dialog = useDialog()

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

  // 计算视口范围内的列
  const visibleStartX = -offsetX;
  const visibleEndX = canvasWidth - offsetX;
  const startColumn = Math.max(0, Math.floor(visibleStartX / columnSize));
  const endColumn = Math.min(notes.value.length, Math.ceil(visibleEndX / columnSize));

  ctx.clearRect(0, 0, canvasWidth, canvasHeight);
  ctx.save();
  ctx.translate(offsetX, 0);
  
  // 绘制网格（仅在可见区域内）
  ctx.strokeStyle = "rgba(85, 85, 85, 0)";
  const startGridX = Math.floor(visibleStartX / gridSize) * gridSize;
  const endGridX = Math.ceil(visibleEndX / gridSize) * gridSize;
  
  for (let x = startGridX; x <= endGridX; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvasHeight);
    ctx.stroke();
  }
  for (let y = 0; y < canvasHeight; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(startGridX, y);
    ctx.lineTo(endGridX, y);
    ctx.stroke();
  }
  
  // 绘制列线
  ctx.strokeStyle = "rgba(136, 136, 136, 0.7)";
  ctx.lineWidth = 2;
  
  // 如果视野内只有一列，绘制完整的分割线
  if (endColumn - startColumn <= 1) {
    for (let x = 0; x < canvasWidth - offsetX; x += columnSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvasHeight);
      ctx.stroke();
    }
  } else {
    // 否则只绘制可见区域的分割线
    for (let x = startColumn * columnSize; x <= endColumn * columnSize; x += columnSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvasHeight);
      ctx.stroke();
    }
  }
  
  ctx.lineWidth = 1;
  ctx.fillStyle = "#F2C9C4";
  
  // 只绘制视野内的音符
  for (let columnIndex = startColumn; columnIndex < endColumn; columnIndex++) {
    const column = notes.value[columnIndex];
    if (!column) continue;
    
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

      let textToDisplay = "";
      if (durationNotes.value.length === 1) {
        textToDisplay = String(durationNotes.value[0]);
      } else if (columnIndex < durationNotes.value.length) {
        textToDisplay = String(durationNotes.value[columnIndex]);
      }

      ctx.fillText(textToDisplay, x + rectWidth / 2, y + rectHeight / 2);
      ctx.fillStyle = "#F2C9C4";
    });
  }
  
  ctx.restore();
  
  // 高亮当前列
  ctx.fillStyle = "rgba(155, 149, 201, 0.5)";
  const highlightX = currentX > viewportCenter ? viewportCenter : currentX;
  ctx.fillRect(highlightX, 0, columnSize, canvasHeight);
};

const previousColumn=()=>{ 
  if (currentColumn.value >0){ c
    urrentColumn.value--; 
    progress.value=currentColumn.value + 1; 
    drawCanvas();
    playNowColumn();
  }
};
const nextColumn=()=>{ 
  if (currentColumn.value < notes.value.length - 1){ 
    currentColumn.value++; 
    progress.value=currentColumn.value + 1; 
    drawCanvas();
    playNowColumn();
  }
};
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

const saveFile=(filename, content)=>{ 
  const blob=new Blob([content],{ type: "text/plain"}); 
  const a=document.createElement("a"); 
  a.href=URL.createObjectURL(blob); 
  a.download=filename; 
  document.body.appendChild(a); 
  a.click(); 
  document.body.removeChild(a); 
  URL.revokeObjectURL(a.href);
}
async function handleUploadSheet(options: { file: any; fileList: UploadFileInfo[] }) {
  loadFile(options.file.file.path)
}

async function loadFile(filePath) {
  try {
    const res = await window.api.readFile(filePath, true);
    if (!res || !Array.isArray(res) || res.length === 0) {
      throw new Error('谱子数据格式错误');
    }
    const { name = '未知文件', songNotes = [] } = res[0];
    fileName.value = name;
    if (!Array.isArray(songNotes)) {
      throw new Error('谱子音符数据格式错误');
    }
    pause()
    notes.value = [];
    durationNotes.value = [];
    timeNotes.value = [];
    const timeGroupedNotes = new Map();
    songNotes.forEach(note => {
      if (!timeGroupedNotes.has(note.time)) {
        timeGroupedNotes.set(note.time, {
          time: note.time,
          keys: [],
          duration: note.duration || 0
        });
      }
      timeGroupedNotes.get(note.time).keys.push(note.key);
    });
    const sortedNotes = Array.from(timeGroupedNotes.values())
      .sort((a, b) => a.time - b.time);
    sortedNotes.forEach((item, index) => {
      const keyNumbers = item.keys.map(key => {
        const match = key.match(/(Key-?\d+)/);
        return match ? Number(match[0].replace('Key', '')) + 1 : 0;
      }).filter(num => num !== 0);
      notes.value.push(keyNumbers);
      durationNotes.value.push(item.duration);
      timeNotes.value.push(
        index < sortedNotes.length - 1 ? 
        sortedNotes[index + 1].time - item.time : 
        0
      );
    });
    syncCanvasToKeysArea();
    drawCanvas();
    currentColumn.value = 0;
    progress.value = 1;
    message.success('谱子加载成功');
  } catch (error) {
    message.error(`谱子加载失败: ${error}`);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let isFirst = true
const play = async () => { 
  if (intervalId.value) return; // 避免重复启动
  if (currentColumn.value >= notes.value.length - 1) {
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
  console.log(currentColumn.value)
  if (currentColumn.value == 0) {
    currentColumn.value = notes.value.length
    progress.value = notes.value.length
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
const deleteCurrentColumn=()=>{ 
  notes.value.splice(currentColumn.value, 1); 
  durationNotes.value.splice(currentColumn.value, 0); 
  if (currentColumn.value >=notes.value.length){ 
    currentColumn.value=notes.value.length - 1;
  } progress.value=currentColumn.value + 1; 
  drawCanvas();
};
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

onMounted(()=>{ 
  window.api.window_size(774,1500); 
  const canvas:any=midiCanvas.value; 
  if (canvas){ 
    canvas.width=canvasWidth; 
    canvas.height=canvasHeight; 
    drawCanvas(); 
    getListData('systemMusic');
    syncCanvasToKeysArea();
  }
});
onUnmounted(()=>{ 
  pause(); 
  window.api.window_size(0,0);
});

onBeforeRouteLeave((_to, _from, next) => {
  if (notes.value.length >= 3){
    dialog.warning({
      title: '一个来自开发者的温馨小提示⭐',
      content: '确定要离开乐谱编辑页面吗？未保存的更改将丢失。',
      positiveText: '就走就走',
      negativeText: '不走了我先保存吧',
      maskClosable: false,
      onMaskClick: () => {
        next(false); // 阻止离开
      },
      onPositiveClick: () =>{
        next();
      },
      onNegativeClick: ()=>{
        next(false); // 阻止离开
      }
    })
  }else{
    next();
  }
});
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
:deep(.n-tabs){
    --n-tab-text-color-active: rgb(242,232,196)!important;
    --n-tab-text-color-hover: rgb(242,232,196)!important;
    --n-tab-text-color: rgb(221,242,196)!important;
}
:deep(.td_css td) {
  color: rgb(242,232,196) !important;
}
:deep(.th_css){
  color: rgb(221,242,196) !important;
}

:deep(.table_position td) {
  background-color: rgba(242, 201, 196, 0.507) !important;
}
:deep(.n-tabs-bar){
  --n-bar-color: rgb(242,232,196)!important;
}
</style>
