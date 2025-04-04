import { app, shell, BrowserWindow, ipcMain, screen, Notification, powerSaveBlocker } from 'electron'
import { join } from 'path'
import { electronApp, is } from '@electron-toolkit/utils'
import icon from '../../build/icon.png?asset'
import { exec } from 'child_process'
import Store from 'electron-store';
const path = require('path')
const fs = require('fs');
const iconv = require('iconv-lite'); // 用于支持多种编码格式

let mainWindow: BrowserWindow | null = null;

Store.initRenderer()
const elStore = new Store()

app.commandLine.appendSwitch('no-sandbox');
// 启动电源保护
powerSaveBlocker.start('prevent-display-sleep');
powerSaveBlocker.start('prevent-app-suspension');
app.commandLine.appendSwitch('enable-gpu-rasterization');  // 强制 GPU 光栅化
app.commandLine.appendSwitch('ignore-gpu-blacklist');  // 忽略 Electron GPU 黑名单
app.commandLine.appendSwitch('force-color-profile', 'srgb');  // 统一颜色配置
app.commandLine.appendSwitch('disable-background-timer-throttling'); // 关闭后台定时器节流
// 允许 GPU 但在必要时自动回退到软件渲染
app.commandLine.appendSwitch('disable-software-rasterizer');
function createWindow(): void {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 774,
    resizable: false,
    autoHideMenuBar: true,
    frame: false,
    transparent: true,
    alwaysOnTop: false,
    icon,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false,
      nodeIntegration: false,
      contextIsolation: true
    }
  })
  mainWindow.on('ready-to-show', () => {
    mainWindow?.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    // Menu.setApplicationMenu(null)
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }

  // 窗口拖动逻辑
  let isMousePressed = false
  let offsetX = 0
  let offsetY = 0
  let nowHeight = 774
  let nowWidth = 800

  ipcMain.on('mousedown', (_event, { }) => {
    console.log(_event)
    const cursorPoint = screen.getCursorScreenPoint()
    let bounds:any = null
    bounds = mainWindow?.getBounds()
    if (bounds) {
      isMousePressed = true
      offsetX = cursorPoint.x - bounds.x // 精确鼠标偏移量
      offsetY = cursorPoint.y - bounds.y
    }
  })

  ipcMain.on('mousemove', (event) => {
    console.log(event)
   if (isMousePressed && mainWindow) {
     const cursorPoint = screen.getCursorScreenPoint()
     // 实时更新窗口位置
     mainWindow.setBounds({
       x: cursorPoint.x - offsetX,
       y: cursorPoint.y - offsetY,
       width: nowWidth,
       height: nowHeight
     })
   }
  })

  ipcMain.on('mouseup', () => {
    isMousePressed = false
  })

  ipcMain.on('window-min', (event) => {
    console.log(event)
    mainWindow?.minimize()
  })

  ipcMain.on('window-close', (event) => {
    console.log(event)
    exec("taskkill /f /im Sky_Music.exe")
    ipcMain.removeAllListeners('mousedown')
    ipcMain.removeAllListeners('mousemove')
    ipcMain.removeAllListeners('mouseup')
    mainWindow?.close()
    app.quit()
  })

  ipcMain.on('set-always-on-top', (event) => {
    console.log(event)
    mainWindow?.setAlwaysOnTop(!mainWindow?.isAlwaysOnTop())
  })

  ipcMain.on('send_system_notification', (_event, title:string, body: string) => {
    const notification = new Notification({title,body});
    notification.show();  // 显示通知
    setTimeout(()=>{
      notification.close()
    },1500)
  })


  ipcMain.on('window_size', (_event, height:number, width: number) => {
    console.log(_event)
    let bounds:any = null
    bounds = mainWindow?.getBounds()

    nowHeight = height === 0 ? 774 : height
    nowWidth = width === 0 ? 800 : width
    mainWindow?.setBounds({
      x: bounds.x,
      y: bounds.y,
      width:nowWidth,
      height:nowHeight
    })
  })

  ipcMain.handle('read-file', async (_event, filePath:string, needData: boolean) => {
    try {
      let fileContent = await fs.promises.readFile(filePath, 'utf8');
      const encodingList = ['utf8', 'utf16le', 'gbk']; // 支持的编码
      for (const encoding of encodingList) {
        try {
          const buffer = await fs.promises.readFile(filePath);
          fileContent = iconv.decode(buffer, encoding);
          // 测试解析（假设文件是 JSON 格式）
          JSON.parse(fileContent); // 尝试解析
          break; // 成功解析则退出循环
        } catch (err) {
          // 如果解析失败，继续尝试下一个编码
          fileContent = undefined;
        }
      }
      if (needData){
        return JSON.parse(fileContent)
      }
      return fileContent.includes("songNotes")
    } catch (err) {
      console.error('Error loading JSON:', err);
      return false;
    }
  });

  ipcMain.handle('getVersion', (_event) => {
    return app.getVersion()
  });

  // console.log('当前缓存存储位置',app.getPath('userData'))
  ipcMain.on('setElStore', (_event, key, value) => {
    elStore.set(key, value)
  })

  ipcMain.on('getElStore', (event, key) => {
    const result = elStore.get(key)
    event.returnValue = result
  })
}

app.on('window-all-closed', () => {
  app.quit();
})

app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.windhide')
  createWindow()
  let runPath = __dirname.replace("resources\\app.asar\\out\\main","")
  const serverPath = path.join(runPath, 'backend_dist/sky-music-server/sky-music-server.exe')
  const command = `"${serverPath}"`;
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing exe as admin: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
  })
})

