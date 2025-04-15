<template>
  <div class="father">
    <n-divider>
        ⚠
    </n-divider>
    <div class="father">
      <n-highlight style="margin-bottom: 5px" :text="headText" :patterns="patterns" :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2E8C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }" />
      <n-highlight style="margin-bottom: 5px" :text="headText2" :patterns="patterns" :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2E8C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }" />
      <n-highlight style="margin-bottom: 5px" :text="headText3" :patterns="patterns" :highlight-style="{
        padding: '0 6px',
        margin: '0 6px',
        borderRadius: themeVars.borderRadius,
        display: 'inline-block',
        color: 'black',
        background: '#F2E8C4',
        transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
      }" />
      <n-divider />
      <div class="father">
        <n-space style="width: 100%;" align='center' justify='center'>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('Y')">Y</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('U')">U</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('I')">I</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('O')">O</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('P')">P</n-button>
        </n-space>
        <n-space class="dynamicSpaceStyles" align='center' justify='center'>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('H')">H</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('J')">J</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('K')">K</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('L')">L</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress(';')">;</n-button>
        </n-space>
        <n-space class="dynamicSpaceStyles" align='center' justify='center'>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('N')">N</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('M')">M</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress(',')">,</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('.')">.</n-button>
          <n-button class="dynamicButtonStyles" ghost @click="keypress('/')">/</n-button>
        </n-space>
      </div>
      <n-divider />
      <div class="father" v-for="button in buttons">
        <n-button dashed :color=button.color @click="run(button.value)"
          :style="{ marginTop: '10px', marginLeft: button.value === 'autoFire' ? '0px' : '15px' }"
          v-if="button.value != 'developer' && button">
          {{ button.context }}
        </n-button>
        <n-upload v-else action="http://localhost:9899/autoScriptUpload" style="margin-top:10px; margin-left: 15px;" accept=".txt"
          :show-file-list="false">
          <n-button type="info" dashed :color=button.color> {{ button.context }}</n-button>
        </n-upload>
      </div>
      <n-input-group class="father" style="margin-top: 20px;">
        <n-select v-model:value="selectValue" :options="options" style="width: 15%;" />
        <n-input-number v-model:value="mathValue" clearable step="0.01" style=" margin-left: 20px; width: 20%;" />
        <n-button type="error" dashed style="margin-left: 20px;" @click="checkFile">
          {{ t('magic_tools.buttons.check') }}
        </n-button>
        <n-input-number style="margin-left: 10px !important; width: 30%;" v-model:value="QCount" />
        <n-button type="primary" @click="run('alwaysQ')" dashed >
          {{ t('magic_tools.buttons.abaaba') }}
        </n-button>
      </n-input-group>
      <n-input-group  style="flex: 0 0 100%; margin-top: 10px;" class="father">
      </n-input-group>
    </div>
    <n-divider />
    <div class="father" v-for="button in fileButtons">
        <n-button dashed :color=button.color @click="openFileHandle(button.value)"
          :style="{ marginTop: '20px', marginLeft: button.value === 'systemMusic' ? '0' : '15px' }">
          {{ button.context }}
        </n-button>
      </div>
  </div>
</template>

<script setup lang="ts">
import { sendData } from "@renderer/utils/fetchUtils";
import { useThemeVars } from "naive-ui";
import { ref } from "vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const themeVars = useThemeVars();
const headText = t("magic_tools.head_text");
const headText2 = t("magic_tools.head_text2");
const headText3 = t("magic_tools.head_text3");
const patterns = [t("magic_tools.patterns1"),t("magic_tools.patterns2"),t("magic_tools.patterns3")]
let mathValue = ref(0.5)
let selectValue = ref("image")
const QCount = ref(300)
const options = [
  {
    label: t('magic_tools.buttons.heart_fire'),
    value: 'image'
  },
  {
    label: t('magic_tools.buttons.key'),
    value: 'key'
  }
]
const buttons = [
  {
    color:"#F2C97D",
    context:t('magic_tools.buttons.autoFire'),
    value: "autoFire"
  },
  {
    color:"#fe6673",
    context:t('magic_tools.buttons.developer'),
    value: "developer"
  },{
    color:"#ff0000",
    context:t('magic_tools.buttons.shutdown'),
    value: "shutdown"
  },
]

const fileButtons = [
  {
    color:"#afdfe4",
    context:t('magic_tools.fileButtons.systemMusic'),
    value: "systemMusic"
  },
  {
    color:"#45b97c",
    context:t('magic_tools.fileButtons.myImport'),
    value: "myImport"
  },
  {
    color:"#ea66a6",
    context:t('magic_tools.fileButtons.myTranslate'),
    value: "myTranslate"
  },
  {
    color:"#ef4136",
    context:t('magic_tools.fileButtons.myFavorite'),
    value: "myFavorite"
  },
  {
    color:"#9b95c9",
    context:t('magic_tools.fileButtons.translateMID'),
    value: "translateMID"
  }
]

function run(value: any){
  console.log(value)
  switch(value){
    case 'shutdown':
      shutdown()
      break;
    case 'alwaysQ':
      for ( let i = 0 ; i <= QCount.value; i++){
        keypress('Q')
      }
      break;
    case 'autoFire':
      autoClickFire()
      break;
  }
}

function checkFile(){
  sendData("test",{
    operate:selectValue.value,
    conf:mathValue.value
  })
}

function keypress(key){
  sendData("test",{
    operate:'press',
    key
  })
}

function autoClickFire(){
  window.api.system_notification("🔧🔧🔧🔧🔧", t('magic_tools.messeage.start'))
  sendData("auto", {
    "operate":"click_fire"
  })
}

function shutdown(){
  window.api.system_notification("⛔⛔⛔⛔⛔", t('magic_tools.messeage.stop'))
  sendData("auto", {
    "operate":"shutdown"
  })
}

function openFileHandle(type) {
  sendData('openFiles',{
      "operate":"files",
      "type":type
  })
}

</script>

<style scoped>
.father {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.dynamicButtonStyles{
    height: 50px;
    width: 50px;
    margin-left: 5px;
    font-size: 20px;
}
.dynamicSpaceStyles{
  margin-top: 10px;
}
</style>
