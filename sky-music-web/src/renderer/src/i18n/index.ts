import { createI18n } from 'vue-i18n'
import zh_cn from './locales/zh-cn.json'
import zh_classical from './locales/zh-classical.json'
import zh_tw from './locales/zh-tw.json'
import en from './locales/en.json'
import jp from './locales/jp.json'
import ko from './locales/ko.json'

// 从localStorage获取保存的语言设置，如果没有则使用默认值'zh_cn'
const savedLanguage = localStorage.getItem('sky-music-language') || 'zh_cn'

const i18n = createI18n({
  legacy: false,
  locale: savedLanguage,
  fallbackLocale: 'zh_cn',
  messages: {
    zh_cn,
    zh_classical,
    zh_tw,
    en,
    jp,
    ko
  }
})

export default i18n