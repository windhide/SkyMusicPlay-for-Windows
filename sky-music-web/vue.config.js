const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  pluginOptions: {
    electronBuilder: {
      appId: 'com.windhide.sky',
      productName: 'Sky_Music',
      directories: {
        output: 'dist_electron',
      },
      // 将 icon 配置移到这里
      build: {
        win: {
          icon: 'public/favicon.ico', // 确保图标路径正确
        },
      },
    },
  },
});
