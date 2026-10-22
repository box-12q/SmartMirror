const { contextBridge, ipcRenderer } = require('electron');

/**
 * Expose a minimal, safe API to the renderer process.
 * The gesture-related IPC handlers will be added here later.
 */
contextBridge.exposeInMainWorld('api', {
  // Intentionally empty for now.
  // Example (once we have IPC channels):
  //   onGestureEvent: (callback) => ipcRenderer.on('gesture', (_e, data) => callback(data)),
});
