import { app, shell, BrowserWindow, ipcMain, screen } from 'electron'
import { join } from 'path'
import { electronApp, is } from '@electron-toolkit/utils'
import icon from '../../build/icon.png?asset'
import { exec } from 'child_process'
const path = require('path')
const fs = require('fs');

let mainWindow: BrowserWindow | null = null;
let modal: BrowserWindow | null = null;
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

  ipcMain.on('mousedown', (_event, { }) => {
    const senderWebContents = _event.sender;  // 获取发送消息的 webContents
    const cursorPoint = screen.getCursorScreenPoint()
    let bounds:any = null

    if (senderWebContents === mainWindow?.webContents) {
      bounds = mainWindow?.getBounds()
    } else if (senderWebContents === modal?.webContents) {
      bounds = modal?.getBounds()
    }


    if (bounds) {
      isMousePressed = true
      offsetX = cursorPoint.x - bounds.x // 精确鼠标偏移量
      offsetY = cursorPoint.y - bounds.y
    }
  })

  ipcMain.on('mousemove', (event) => {
    const senderWebContents = event.sender;  // 获取发送消息的 webContents

    if (senderWebContents === mainWindow?.webContents) {
      if (isMousePressed && mainWindow) {
        const cursorPoint = screen.getCursorScreenPoint()
        // 实时更新窗口位置
        mainWindow.setBounds({
          x: cursorPoint.x - offsetX,
          y: cursorPoint.y - offsetY,
          width: 800,
          height: 774
        })
      }
    } else if (senderWebContents === modal?.webContents) {
      if (isMousePressed && modal) {
        const cursorPoint = screen.getCursorScreenPoint()
        // 实时更新窗口位置
        modal.setBounds({
          x: cursorPoint.x - offsetX,
          y: cursorPoint.y - offsetY,
          width: 600,
          height: 400
        })
      }
    }
  })

  ipcMain.on('mouseup', () => {
    isMousePressed = false
  })

  ipcMain.on('window-min', (event) => {
    const senderWebContents = event.sender;  // 获取发送消息的 webContents
    if (senderWebContents === mainWindow?.webContents) {
      mainWindow?.minimize()
    } else if (senderWebContents === modal?.webContents) {
      modal?.minimize()
    }
  })

  ipcMain.on('window-close', (event) => {
    const senderWebContents = event.sender;  // 获取发送消息的 webContents
    if (senderWebContents === mainWindow?.webContents) {
      if (!modal?.isDestroyed()) {
        modal?.close();
      }
      mainWindow?.close()
    } else if (senderWebContents === modal?.webContents) {
      modal?.close()
    }
  })

  ipcMain.on('set-always-on-top', (event) => {
    const senderWebContents = event.sender;  // 获取发送消息的 webContents
    if (senderWebContents === mainWindow?.webContents) {
      mainWindow?.setAlwaysOnTop(!mainWindow?.isAlwaysOnTop())
    } else if (senderWebContents === modal?.webContents) {
      modal?.setAlwaysOnTop(!modal?.isAlwaysOnTop())
    }  
  })

  ipcMain.handle('read-file', async (_event, filePath) => {
    try {
      console.log(`Checking file: ${path}`);
      const fileContent = await fs.promises.readFile(filePath, 'utf8');
      const jsonData = JSON.parse(fileContent);
      if (
        jsonData &&
        Array.isArray(jsonData) &&
        jsonData.length > 0 &&
        jsonData[0].hasOwnProperty('songNotes')
      ) {
        return true;
      } else {
        return false;
      }
    } catch (err) {
      console.error('Error loading JSON:', err);
      return false;
    }
  });

  ipcMain.on('open-tutorial', () => {
    let root_path;
    if (is.dev) {
      root_path = "http://127.0.0.1:5173/";
    } else {
      root_path = join(__dirname, '../renderer/index.html')
    };
    modal = new BrowserWindow({
      width: 600,
      height: 400,
      hasShadow: true, // 阴影 
      resizable: false, // 禁止调整窗口大小
      frame: false,     // 禁用默认的窗口框架（包括菜单和标题栏）
      transparent: true,
      webPreferences: {
        preload: join(__dirname, '../preload/index.js'),
        sandbox: false,
        nodeIntegration: false,
        contextIsolation: true
      },
    });
    modal.loadURL(root_path);
  });


  mainWindow.on('closed', () => {
    ipcMain.removeAllListeners('mousedown')
    ipcMain.removeAllListeners('mousemove')
    ipcMain.removeAllListeners('mouseup')
    app.exit()
  })

}

app.on('window-all-closed', () => {
  app.exit()
})

app.disableHardwareAcceleration(); // 禁用gpu加速


app.whenReady().then(() => {
  // Set app user model id for windows
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

