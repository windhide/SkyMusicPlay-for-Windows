
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
    window.elStore.setElStore(key, value)
  },

  getItem: (key) => {
    const value = window.elStore.getElStore(key)
    return value
  }
}

export default configStore
