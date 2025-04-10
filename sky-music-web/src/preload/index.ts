import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'
// Custom APIs for renderer
const api = {}
// @ts-ignore (define in dts)
const elStore = {}

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
      sync_el_2_sheet:() => {
        ipcRenderer.send('sync_el_2_sheet');
      },
      sync_sheet_2_el:() => {
        ipcRenderer.send('sync_sheet_2_el');
      }
    });// 用于向主进程发送拖动事件
    contextBridge.exposeInMainWorld('electron', {
      onMouseDown: (x, y) => ipcRenderer.send('mousedown', { x, y }),
      onMouseMove: (x, y) => ipcRenderer.send('mousemove', { x, y }),
      onMouseUp: () => ipcRenderer.send('mouseup')
    })
    // 用于数据持久化
    contextBridge.exposeInMainWorld('elStore', {
      setElStore:(key, value)=>{
        ipcRenderer.send('setElStore', key, value);
      },
      getElStore:(key)=>{
        return ipcRenderer.sendSync('getElStore', key);
      }
    })
  } catch (error) {
    console.error(error)
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI
  // @ts-ignore (define in dts)
  window.api = api
  // @ts-ignore (define in dts)
  window.elStore = elStore
}
