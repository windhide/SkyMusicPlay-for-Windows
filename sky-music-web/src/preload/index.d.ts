import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    api: {
      setAlwaysOnTop: () => void;
      close: () => void;
      mini: () => void;
      async readFile: (filePath:string) => any;
      system_notification: (title,body) => void;
      getVersion: () => any,
    };
    electron:{
      onMouseDown: (x, y) => void;
      onMouseMove: (x, y) => void;
      onMouseUp: ()=> void;
  }
  }
}
