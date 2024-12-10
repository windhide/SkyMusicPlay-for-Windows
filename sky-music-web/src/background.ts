'use strict'

import { app, protocol, BrowserWindow, Menu } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
const isDevelopment = process.env.NODE_ENV !== 'production'

// 打包用的
var cmd=require('node-cmd');
var currentPath = require("path").dirname(require('electron').app.getPath("exe"));

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 774,
    resizable: false,  // 禁止调整窗口
    icon: `${__dirname}/public/favicon.ico`, // 添加这一行来设置应用图标
    webPreferences: {
      webSecurity: false,
      nodeIntegration: (process.env
          .ELECTRON_NODE_INTEGRATION as unknown) as boolean,
      contextIsolation: !(process.env
          .ELECTRON_NODE_INTEGRATION as unknown) as boolean
    }
  })
  if (process.env.WEBPACK_DEV_SERVER_URL) {
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL as string)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    Menu.setApplicationMenu(null) //取消菜单栏
    createProtocol('app')
    win.loadURL('app://./index.html')
  }
}
app.on('window-all-closed', () => {
    app.quit()
    cmd.run(`runas /user:Administrator "taskkill /F /im sky-music-server.exe"`)
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    try {
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e)
    }
  }
  // 启动服务器exe
  cmd.run(`${currentPath}/backend_dist/sky-music-server/sky-music-server.exe`,function(err, data, stderr){
    console.log(data)
    console.log(err)
    console.log(stderr)
  });

  createWindow()
})
