'use strict'

import { app, protocol, BrowserWindow, Menu } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
const isDevelopment = process.env.NODE_ENV !== 'production'

// 打包用的
var cmd=require('node-cmd');
var currentPath = require("path").dirname(require('electron').app.getPath("exe"));

// Menu.setApplicationMenu(null) //取消菜单栏

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow() {
  // Create the browser window.
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
  win.webContents.openDevTools()
  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL as string)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
    app.quit()
    cmd.run(`taskkill /F /im sky_windows_music.exe`)
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e)
    }
  }
  // console.log("now start service")
  // console.log(`${currentPath}/backend_dist/sky_windows_music/sky_windows_music.exe`)
  // 启动服务器exe
  cmd.run(`${currentPath}/backend_dist/sky_windows_music/sky_windows_music.exe`,function(err, data, stderr){
    console.log(data)
    console.log(err)
    console.log(stderr)
  });

  createWindow()
})

app.on('before-quit', () => {
  // 退出前执行的操作，如关闭后端
  cmd.run(`taskkill /F /im sky_windows_music.exe`)
});

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
        // 关闭服务器exe
        cmd.run(`taskkill /F /im sky_windows_music.exe`)
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
      cmd.run(`taskkill /F /im sky_windows_music.exe`)
    })
  }
}