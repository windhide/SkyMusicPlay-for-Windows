import { app, shell, BrowserWindow, ipcMain, screen, Notification, powerSaveBlocker } from 'electron'
import { join } from 'path'
import { electronApp, is } from '@electron-toolkit/utils'
import icon from '../../build/icon.png?asset'
import { spawn, execSync } from 'child_process'
import Store from 'electron-store';
Store.initRenderer()
const path = require('path')
const fs = require('fs');
const iconv = require('iconv-lite'); // 用于支持多种编码格式
const elStore = new Store()
const MAX_CONCURRENT_COPIES = 20; // 限制最大并行任务数
let limit;
(async () => {
  const { default: pLimit } = await import('p-limit');
  limit = pLimit(MAX_CONCURRENT_COPIES);
})();
let mainWindow: BrowserWindow | null = null;

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
const syncFolders = ["myImport", "myTranslate", "myFavorite"]
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

  ipcMain.on('sync_sheet_2_el', async (_event,) =>{
    let cachePath = elStore.path.replaceAll("\\config.json", "");
      for (const folder of syncFolders) {
        fetch("http://127.0.0.1:9899/path", {
            method: 'POST', 
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              "type": folder
            }), 
          }).then(response => response.json())
          .then(data =>{
            copyFolderIncremental(data, path.join(cachePath, folder));
          })
          .catch(error => console.error(error))
      }
  })

  ipcMain.on('sync_el_2_sheet', async (_event,) =>{
    let cachePath = elStore.path.replaceAll("\\config.json", "");
    for (const folder of syncFolders) {
      fetch("http://127.0.0.1:9899/path", {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "type": folder
        }), 
      }).then(response => response.json()).then(data =>{ 
        copyFolderIncremental(path.join(cachePath, folder), data);
      }).catch(error => console.error(error))
    }
  })

  async function copyFolderIncremental(source, target) {
    try {
        target = path.resolve(target);
        source = path.resolve(source);
        console.log("target=>", target);
        console.log("source=>", source);
        // 检查源文件夹是否存在
        let sourceExists = true;
        try {
            await fs.promises.access(source, fs.constants.F_OK);
        } catch (err) {
            sourceExists = false;
            await fs.promises.mkdir(source, { recursive: true });
        }
        // 检查目标文件夹是否存在
        let targetExists = true;
        try {
            await fs.promises.access(target, fs.constants.F_OK);
        } catch (err) {
            targetExists = false;
        }
        // 如果源文件夹不存在且目标文件夹存在，删除目标文件夹
        if (!sourceExists && targetExists) {
            await fs.promises.rm(target, { recursive: true, force: true });
        }
        // 确保目标文件夹存在
        await fs.promises.mkdir(target, { recursive: true });
        // 获取源文件夹中的文件列表
        const sourceFiles = await fs.promises.readdir(source);
        const sourceFilesSet = new Set(sourceFiles);
        // 如果目标文件夹存在，检查需要删除的文件
        if (targetExists) {
            const targetFiles = await fs.promises.readdir(target);
            const deletePromises = targetFiles
                .filter(file => !sourceFilesSet.has(file))
                .map(file => {
                    const targetPath = path.join(target, file);
                    return fs.promises.rm(targetPath, { recursive: true, force: true });
                });
            await Promise.all(deletePromises);
        }
        // 复制或更新文件
        const copyTasks = sourceFiles.map(file => limit(async () => {
            try {
                const sourcePath = path.join(source, file);
                const targetPath = path.join(target, file);
                const sourceStats = await fs.promises.stat(sourcePath);

                if (sourceStats.isFile()) {
                    let shouldCopy = true;
                    try {
                        const targetStats = await fs.promises.stat(targetPath);
                        shouldCopy = targetStats.mtimeMs < sourceStats.mtimeMs;
                    } catch (err) {
                        // 目标文件不存在，需要复制
                    }
                    if (shouldCopy) {
                        await fs.promises.copyFile(sourcePath, targetPath);
                    }
                } else if (sourceStats.isDirectory()) {
                    await copyFolderIncremental(sourcePath, targetPath);
                }
            } catch (err) {
                console.error(`Error processing file ${file}:`, err);
            }
        }));
        await Promise.all(copyTasks);
    } catch (err) {
        console.error("Error copying folder:", err);
        console.log("Continuing with other operations...");
    }
  }


}

app.on('window-all-closed', () => {
  app.quit();
})

function launchBackend() {
  const args = ['--prod']
  const exeName = 'sky_music_server.exe'
  let runPath = __dirname.replace("resources\\app.asar\\out\\main","")
  const exePath = path.join(runPath, 'backend_dist/sky_music_server/sky_music_server.exe')

  if (!fs.existsSync(exePath)) {
    console.error('[server] server File not found:', exePath)
    return
  }

  if (isBackendRunning(exeName)) {
    console.log('[server] is running, do Nothiong')
    return
  }

  console.log('[server] starting:', exePath)

  const subprocess = spawn(exePath, args, {
    detached: true,
    stdio: 'ignore',
    windowsHide: true
  })

  subprocess.unref() // 让它在主进程退出后仍能运行
}

function isBackendRunning(processName: string): boolean {
  try {
    const stdout = execSync('tasklist', { encoding: 'utf-8' })
    return stdout.toLowerCase().includes(processName.toLowerCase())
  } catch (err) {
    console.error('[check server] faild:', err)
    return false
  }
}


app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.windhide')
  createWindow()
  launchBackend()
})

