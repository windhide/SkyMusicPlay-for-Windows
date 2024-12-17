const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  pluginOptions: {
    electronBuilder: {
      appId: 'com.windhide.sky',
      productName: 'Sky_Music',
      author: "WindHide <WindHide520@gmail.com>",
      directories: {
        output: 'dist_electron', // 输出目录
      },
      extraResources: [
        {
          from: 'public/icon.ico', // 指定 public 文件夹
          to: 'public/icon.ico'
        },
        {
          from: 'src/preload.ts', // 确保包含 preload.ts 文件
          to: 'src/preload.ts',
        },
      ],
      builderOptions: {
        appId: 'com.windhide.sky',
        productName: 'Sky_Music',
        directories: {
          output: 'dist_electron',
        },
        files: [
          '**/*', // 包含所有源文件
          '!**/tests/**', // 排除测试文件
          'dist/**/*' // 包括编译后的 dist 文件夹内容
        ],
        win: {
          icon: 'public/icon.ico', // 指定 Windows 的图标
          requestedExecutionLevel: 'requireAdministrator', // 需要管理员权限
        }
      },
      chainWebpackMainProcess: (config) => {
        config.output.filename('background.js'); // 修改主进程输出文件名
      },
    },
  },
});
