<template>
    <n-flex align="center">
        <n-gradient-text :size="20" type="success" style="width: 100%">
            {{ "当前: " + nowPlayMusic + "" }}
        </n-gradient-text>
        <n-button type="primary" ghost @Click="transferPDF" :loading="processFlag">
            转PDF
        </n-button>
        <n-gradient-text type="warning">
            ⭐
        </n-gradient-text>
        <n-switch :round="false" v-model:value="templateSelect" />
        <n-gradient-text type="info">
            噢
        </n-gradient-text>
    </n-flex>
    <n-card style="margin-top: 20px">
        <n-tabs type="bar" animated @update:value="handleUpdateValue" @before-leave="handleBeforeLeave" size="small">
            <n-tab-pane name="systemMusic" tab="自带歌曲" >
        <n-data-table :columns="musicColumns" :data="music.systemMusic" :bordered="false" :min-row-height="48"  :max-height="300" :virtual-scroll="music.systemMusic.length > 7" 
          :row-props="systemMusicSelect"/>
        </n-tab-pane>
        <n-tab-pane name="myImport" tab="导入歌曲">
          <n-data-table :columns="musicColumns" :data="music.myImport" :bordered="false" :min-row-height="48"  :max-height="300" :virtual-scroll="music.myImport.length > 7"
            :row-props="myImportMusicSelect" />
        </n-tab-pane>
        <n-tab-pane name="myTranslate" tab="转换歌曲">
          <n-data-table :columns="musicColumns" :data="music.myTranslate" :bordered="false" :min-row-height="48"  :max-height="300" :virtual-scroll="music.myTranslate.length > 7"
          :row-props="myTranslateMusicSelect" />
        </n-tab-pane>
        <n-tab-pane name="myFavorite" tab="收藏">
          <n-data-table :columns="musicColumns" :data="music.myFavorite" :bordered="false" :min-row-height="48"  :max-height="300" :virtual-scroll="music.myFavorite.length > 7"
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
    <div id="content" style="background-color: black;">
        <div class="sheet" v-for="(sheet,index) in convertSheet" :key="index">
            <n-divider title-placement="left" style="margin-bottom: 10px !important">
                {{ index+1 }}
            </n-divider>
          <n-space>
            <n-button class="buttonStyle" :type="sheet.includes('y') ? 'primary' : 'default'" ghost>{{sheet.includes("y") ? (templateSelect ? 'y' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('u') ? 'primary' : 'default'" ghost>{{sheet.includes('u') ? (templateSelect ? 'u' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('i') ? 'primary' : 'default'" ghost>{{sheet.includes('i') ? (templateSelect ? 'i' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('o') ? 'primary' : 'default'" ghost>{{sheet.includes('o') ? (templateSelect ? 'o' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('p') ? 'primary' : 'default'" ghost>{{sheet.includes('p') ? (templateSelect ? 'p' : '⭐') : ''}}</n-button>
          </n-space>
          <n-space style="margin-top: 10px;">
            <n-button class="buttonStyle" :type="sheet.includes('h') ? 'primary' : 'default'" ghost>{{sheet.includes('h') ? (templateSelect ? 'h' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('j') ? 'primary' : 'default'" ghost>{{sheet.includes('j') ? (templateSelect ? 'j' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('k') ? 'primary' : 'default'" ghost>{{sheet.includes('k') ? (templateSelect ? 'k' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('l') ? 'primary' : 'default'" ghost>{{sheet.includes('l') ? (templateSelect ? 'l' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes(';') ? 'primary' : 'default'" ghost>{{sheet.includes(';') ? (templateSelect ? ';' : '⭐') : ''}}</n-button>
          </n-space>
          <n-space style="margin-top: 10px;">
            <n-button class="buttonStyle" :type="sheet.includes('n')  ? 'primary' : 'default'" ghost>{{sheet.includes('n') ? (templateSelect ? 'n' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('m')  ? 'primary' : 'default'" ghost>{{sheet.includes('m') ? (templateSelect ? 'm' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes(',')  ? 'primary' : 'default'" ghost>{{sheet.includes(',') ? (templateSelect ? ',' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('.')  ? 'primary' : 'default'" ghost>{{sheet.includes('.') ? (templateSelect ? '.' : '⭐') : ''}}</n-button>
            <n-button class="buttonStyle" :type="sheet.includes('/')  ? 'primary' : 'default'" ghost>{{sheet.includes('/') ? (templateSelect ? '/' : '⭐') : ''}}</n-button>
           </n-space>
        </div>
    </div>
</template>

<style scoped>
.buttonStyle {
  height: 75px;
  width: 75px;
}

.sheet {
  height: calc(100vh - 25px - 25px);
  display: flex;
  justify-content: center;
  align-content: center;
  flex-wrap: wrap;
  height: 320px;
}
#content {
    position: relative;
    overflow: visible; /* 确保没有被裁剪 */
    transform: none;   /* 确保没有缩放 */
}
</style>

<script lang="ts" setup>
import { getList, sendData } from "@/utils/fetchUtils";
import { RowData } from "naive-ui/es/data-table/src/interface";
import { reactive, ref, watch, nextTick } from "vue";
import { useMessage } from 'naive-ui'
import { Search } from '@vicons/ionicons5'
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

const message = useMessage()
let convertSheet:any[] = reactive([])

let music: any = reactive({
    // 音乐列表
    systemMusic: [], // 原版音乐
    myImport: [], // 导入的音乐
    myTranslate: [], // 扒谱的音乐
    myFavorite:[]
});
let nowPlayMusic = ref("没有歌曲"); // 当前选中歌曲
let nowType = "systemMusic"
let searchText = ref("")
let musicColumns = [
    {
        title: "歌名",
        key: "name",
    },
]; // 音乐列
const processFlag = ref(false)
let templateSelect = ref(false)

const systemMusicSelect = (row: RowData) => {
    return {
        onClick: () => {
            nowPlayMusic.value = row.name;
        },
    };
};
const myImportMusicSelect = (row: RowData) => {
    return {
        onClick: () => {
            nowPlayMusic.value = row.name;
        },
    };
};
const myTranslateMusicSelect = (row: RowData) => {
    return {
        onClick: () => {
            nowPlayMusic.value = row.name;
        },
    };
};
const myFavoriteMusicSelect = (row: RowData) => {
  return {
    onClick: () => {
      nowPlayMusic.value = row.name;
    },
  };
};

function handleUpdateValue(value: string) {
    searchText.value = ""
    getListData(value)
}

function handleBeforeLeave(name: string){
  nowType = name
  return true;
}

watch(searchText, () => {
    getListData("systemMusic")
    getListData("myImport")
    getListData("myTranslate")
    getListData("myFavorite")
})

async function transferPDF() {
    if (nowPlayMusic.value === "没有歌曲") {
        message.error("选个歌再转换吧靓仔");
        return;
    } else {
        message.success("开始转换")
        processFlag.value = true;
        sendData("getConvertSheet", {
            fileName: nowPlayMusic.value,
            type: nowType,
        })
            .then((res) => {
                convertSheet.push(...res);
            })
            .then(async () => {
                await checkDataLoad();
                const content: any = document.querySelector("#content");
                const canvas = await html2canvas(content, {
                    scale: 1, // 提高分辨率
                    useCORS: true, // 支持跨域图片
                });
                // 获取图片的宽高
                const imgWidth = canvas.width;
                const imgHeight = canvas.height;

                // 计算每张图片的高度（总高度除以 convertSheet 长度）
                const singleImageHeight = 320;

                // 创建 PDF 实例
                const pdf = new jsPDF("p", "mm", [553, 640]);
                const pdfWidth = pdf.internal.pageSize.getWidth();
                const pdfHeight = pdf.internal.pageSize.getHeight();

                let position = 0; // 记录位置
                let pageCount = 0; // 记录页数

                for (let i = 0; i < convertSheet.length; i++) {
                    // 每张图片的高度
                    const adjustedHeight = singleImageHeight;

                    // 创建切片 canvas
                    const pageCanvas = document.createElement("canvas");
                    pageCanvas.width = imgWidth;
                    pageCanvas.height = adjustedHeight;
                    const pageCtx = pageCanvas.getContext("2d");
                    pageCtx?.drawImage(
                        canvas,
                        0,
                        i * singleImageHeight,
                        imgWidth,
                        singleImageHeight,
                        0,
                        0,
                        imgWidth,
                        adjustedHeight
                    );
                    // 转换为图片数据
                    const pageImgData = pageCanvas.toDataURL("image/png");
                    // 每页放两张图片
                    if (position === 0) {
                        pdf.addImage(pageImgData, "PNG", 0, 0, pdfWidth, adjustedHeight);
                        position = 1;
                    } else {
                        // 如果已经放了一张图片，放第二张
                        pdf.addImage(pageImgData, "PNG", 0, adjustedHeight, pdfWidth, adjustedHeight);
                        position = 0; // 重置位置
                        pdf.addPage(); // 新增一页
                    }
                }

                // 保存 PDF
                pdf.save(`${nowPlayMusic.value}.pdf`);
                convertSheet.length = 0
                processFlag.value = false;
                message.success("成功")
            }).catch(()=>{
                message.error("失败，请联系开发者看看啥问题。")
            })
            .finally(() => processFlag.value = false);
    }
}

function checkDataLoad(){
    const content = document.querySelectorAll(".sheet");
    if (content.length === convertSheet.length) {
        return true;
    }
    return checkDataLoad()
}
handleUpdateValue("systemMusic")


function getListData(value){
  getList(value,searchText.value).then(res => {
    eval("music." + value + "=res")
  })
}
</script>