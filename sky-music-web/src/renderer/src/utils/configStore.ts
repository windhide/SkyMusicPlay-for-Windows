import { sendData } from "@renderer/utils/fetchUtils";
export enum CONFIG_TYPE {
  DELAY_STATUS = 'DELAY_STATUS', //间隔延迟状态
  DELAY_SPEED = 'DELAY_SPEED', //延迟设置
  DELAY_RANDOM_START = 'DELAY_RANDOM_START',
  DELAY_RANDOM_END = 'DELAY_RANDOM_END',

  DURATION_STATUS = 'URATION_STATUS', //延音设置状态
  DURATION_SPEED = 'DURATION_SPEED', //延音设置
  DURATION_RANDOM_START = 'DURATION_RANDOM_START',
  DURATION_RANDOM_END = 'DURATION_RANDOM_END',

  PLAY_SPEED = 'PLAY_SPEED', //播放速度

  SHORTCUT_KEY = 'SHORTCUT_KEY' //快捷键配置
}
export enum CONFIG_STATUS_TYPE {
  SYSTEM = 'system',
  RANDOM = 'random',
  CUSTOM = 'custom',
}


const configStore = {
  setItem: (key, value) => {
    // @ts-ignore (define in dts)
    window.elStore.setElStore(key, value)
  },

  getItem: (key) => {
    // @ts-ignore (define in dts)
    const value = window.elStore.getElStore(key)
    return value
  }
}

export default configStore

// 进入程序后，设置缓存快捷键配置
export const setConfigShortcutKey = ()=>{
  if(!configStore.getItem(CONFIG_TYPE.SHORTCUT_KEY)) {
    return
  }
  const shortcutKeyValues = configStore.getItem(CONFIG_TYPE.SHORTCUT_KEY);
  const follow = shortcutKeyValues.follow_key;
  const music = shortcutKeyValues.music_key;
  const followString = (follow.repeat + follow.repeat_next + follow.resize);
  const musicString = (music.next + music.pause + music.resume + music.start + music.stop + music.add_duration + music.reduce_duration + music.add_delay + music.reduce_delay + music.add_speed + music.reduce_speed);
  const followKey = {
    tap_key: "yuiophjkl;nm,./",
    repeat: follow.repeat.toLowerCase(),
    repeat_next: follow.repeat_next.toLowerCase(),
    resize: follow.resize.toLowerCase(),
    exit: follow.exit.toLowerCase(),
    // 使用计算后的字符串
    string: followString.toLowerCase()
  };
  const musicKey = {
    next: music.next.toLowerCase(),
    pause: music.pause.toLowerCase(),
    resume: music.resume.toLowerCase(),
    start: music.start.toLowerCase(),
    stop: music.stop.toLowerCase(),
    string: musicString.toLowerCase(),
    add_duration: music.add_duration.toLowerCase(),
    reduce_duration: music.reduce_duration.toLowerCase(),
    add_delay: music.add_delay.toLowerCase(),
    reduce_delay: music.reduce_delay.toLowerCase(),
    add_speed: music.add_speed.toLowerCase(),
    reduce_speed: music.reduce_speed.toLowerCase(),
  };
  sendData("config_operate", {
    "operate": "set",
    "name": "shortcutStruct",
    "value": {
      "follow_key": followKey,
      "music_key": musicKey
    }
  })
}
