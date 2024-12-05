const { app, BrowserWindow, Menu  } = require('electron')
// const path = require("path")

const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 774,
    resizable: false,  // 禁止调整窗口

    webPreferences: {
      webSecurity: false,
    }
  })

  // 主要改了这里
  // mainWindow.loadFile(path.join(__dirname, "./index.html"));
  // 使用 loadURL 加载 http://localhost:3004 ，也就是我们刚才创建的 Vue 项目地址
  // 3004 改为你 Vue 项目的端口号
  mainWindow.loadURL("http://localhost:8080/");
}
// Menu.setApplicationMenu(null) //取消菜单栏
app.whenReady().then(() => {
  createWindow()
})