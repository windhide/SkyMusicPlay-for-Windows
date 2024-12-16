export {};

declare global {
  interface Window {
    api: {
      setAlwaysOnTop: (isAlwaysOnTop: boolean) => void;
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
