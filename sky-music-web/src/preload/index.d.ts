import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    api: {
      setAlwaysOnTop: () => void;
      close: () => void;
      mini: () => void;
      async readFile: (filePath:string, needData: boolean) => any;
      system_notification: (title,body) => void;
      getVersion: () => any;
      window_size: (height:number, width: number) => void;
      syncElToSheetFiles
      sync_el_2_sheet:() => void;
      sync_sheet_2_el:() =>  void;
    };
    electron:{
      onMouseDown: (x, y) => void;
      onMouseMove: (x, y) => void;
      onMouseUp: ()=> void;
  }
  }
}
