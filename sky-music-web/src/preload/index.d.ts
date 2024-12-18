import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    api: {
      setAlwaysOnTop: () => void;
      open_tutorial: () => void;
      close: () => void;
      mini: () => void;
    };
    electron:{
      onMouseDown: (x, y) => void;
      onMouseMove: (x, y) => void;
      onMouseUp: ()=> void;
  }
  }
}
