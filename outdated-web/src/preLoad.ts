const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  setAlwaysOnTop: (isAlwaysOnTop) => {
    ipcRenderer.send('set-always-on-top', isAlwaysOnTop);
  },
  close: () => {
    ipcRenderer.send('window-close');
  },
  mini: () => {
    ipcRenderer.send('window-min');
  }
});// 用于向主进程发送拖动事件
contextBridge.exposeInMainWorld('electron', {
  onMouseDown: (x, y) => ipcRenderer.send('mousedown', { x, y }),
  onMouseMove: (x, y) => ipcRenderer.send('mousemove', { x, y }),
  onMouseUp: () => ipcRenderer.send('mouseup')
})