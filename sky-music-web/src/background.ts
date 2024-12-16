import { app, protocol, BrowserWindow, ipcMain, screen, Menu } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer'
const isDev = import('electron-is-dev');
const path = require('path')
const cmd = require('node-cmd')

const preloadPath = isDev
  ? path.join(__dirname, '../src/preload.ts')
  : path.join(__dirname, 'preload.js')

const windowIconPath = isDev
  ? path.join(__dirname, '../public/icon.ico')
  : path.join(__dirname, 'icon.ico')

const currentPath = isDev
  ? __dirname
  : require('path').dirname(app.getPath('exe'))

let mainWindow: BrowserWindow | null = null

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow() {
  if (mainWindow) return

  mainWindow = new BrowserWindow({
    width: 800,
    height: 774,
    resizable: false,
    icon: windowIconPath,
    frame: false,
    transparent: true,
    webPreferences: {
      webSecurity: false,
      preload: preloadPath,
      nodeIntegration: false,
      contextIsolation: true
    }
  })

  if (isDev && process.env.WEBPACK_DEV_SERVER_URL) {
    await mainWindow.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    mainWindow.webContents.openDevTools()
  } else {
    Menu.setApplicationMenu(null)
    createProtocol('app')
    mainWindow.loadURL('app://./index.html')
  }

  // 窗口拖动逻辑
  let isMousePressed = false
  let offsetX = 0
  let offsetY = 0

  ipcMain.on('mousedown', (event, { x, y }) => {
    const cursorPoint = screen.getCursorScreenPoint()
    const bounds = mainWindow?.getBounds()

    if (bounds) {
      isMousePressed = true
      offsetX = cursorPoint.x - bounds.x // 精确鼠标偏移量
      offsetY = cursorPoint.y - bounds.y
    }
  })

  ipcMain.on('mousemove', (event) => {
    if (isMousePressed && mainWindow) {
      const cursorPoint = screen.getCursorScreenPoint()

      // 实时更新窗口位置
      mainWindow.setBounds({
        x: cursorPoint.x - offsetX,
        y: cursorPoint.y - offsetY,
        width: mainWindow.getBounds().width,
        height: mainWindow.getBounds().height
      })
    }
  })

  ipcMain.on('mouseup', () => {
    isMousePressed = false
  })

ipcMain.on('window-min', () => {
  mainWindow?.minimize()
})

ipcMain.on('window-close', () => {
  app.quit()
})

ipcMain.on('set-always-on-top', (event, isAlwaysOnTop) => {
  mainWindow.setAlwaysOnTop(!!isAlwaysOnTop)
})

mainWindow.on('closed', () => {
  mainWindow = null
  ipcMain.removeAllListeners('mousedown')
  ipcMain.removeAllListeners('mousemove')
  ipcMain.removeAllListeners('mouseup')
})
}

app.on('ready', async () => {
  if (isDev) {
    try {
      await installExtension(VUEJS_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e)
    }
  }

  const serverPath = path.join(currentPath, 'backend_dist/sky-music-server/sky-music-server.exe')
  cmd.run(serverPath, (err, data, stderr) => {
    console.log(data || 'Backend started.')
    if (err) console.error('Error starting backend:', err)
    if (stderr) console.error('Backend stderr:', stderr)
  })

  if (!mainWindow) {
    createWindow()
  }
})

app.on('window-all-closed', () => {
  app.quit()
})

app.on('before-quit', () => {
  app.quit()
})
