const { contextBridge, ipcRenderer } = require('electron');

/**
 * Minimal, safe API exposed to the renderer process.
 * contextIsolation is on, so the renderer reaches the main process only
 * through these whitelisted calls.
 *
 * Name and method names follow the app convention:
 *   window.electronAPI.minimizeWindow()
 *   window.electronAPI.maximizeWindow()
 *   window.electronAPI.closeWindow()
 * Gesture-related IPC will be added here later.
 */
contextBridge.exposeInMainWorld('electronAPI', {
  minimizeWindow: () => ipcRenderer.send('window:minimize'),
  maximizeWindow: () => ipcRenderer.send('window:maximize'),
  closeWindow: () => ipcRenderer.send('window:close'),
});
