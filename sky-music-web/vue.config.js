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
      extraResources: [
        {
          from: 'resources/', // 确保此文件夹存在且包含要打包的资源
          to: 'resources/', 
          filter: ['**/*']
        }
      ],
      // 将 icon 配置移到这里
      build: {
        win: {
          icon: 'public/favicon.ico', // 确保图标路径正确
        },
      },
    },
  },
});
