const { contextBridge, ipcRenderer } = require('electron');

/**
 * Minimal, safe API exposed to the renderer process.
 * contextIsolation is on, so the renderer reaches the main process only
 * through these whitelisted calls.
 */
contextBridge.exposeInMainWorld('api', {
  minimize: () => ipcRenderer.send('window:minimize'),
  close: () => ipcRenderer.send('window:close'),
  // Gesture-related IPC will be added here later.
});
