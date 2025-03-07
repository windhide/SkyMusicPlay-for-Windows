import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'
// Custom APIs for renderer
const api = {}

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld('api', {
      setAlwaysOnTop: () => {
        ipcRenderer.send('set-always-on-top');
      },
      close: () => {
        ipcRenderer.send('window-close');
      },
      mini: () => {
        ipcRenderer.send('window-min');
      },
      readFile: async (filePath: string, needData: boolean) => {
        return await ipcRenderer.invoke('read-file', filePath, needData); 
      },
      getVersion: () => {
        return ipcRenderer.invoke('getVersion'); 
      },
      system_notification: async (title,body) => {
        ipcRenderer.send('send_system_notification', title, body); 
      },
      window_size: (height:number, width: number) => {
        ipcRenderer.send('window_size', height, width); 
      },
    });// 用于向主进程发送拖动事件
    contextBridge.exposeInMainWorld('electron', {
      onMouseDown: (x, y) => ipcRenderer.send('mousedown', { x, y }),
      onMouseMove: (x, y) => ipcRenderer.send('mousemove', { x, y }),
      onMouseUp: () => ipcRenderer.send('mouseup')
    })
  } catch (error) {
    console.error(error)
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI
  // @ts-ignore (define in dts)
  window.api = api
}
