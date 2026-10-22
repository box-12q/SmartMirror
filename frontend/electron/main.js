const path = require('node:path');
const { app, BrowserWindow, ipcMain } = require('electron');

/** Application window (kept in module scope for IPC handlers below). */
let mainWindow = null;

/**
 * Create the main application window.
 * Frameless (frame: false) + solid background so the window looks clean
 * while the web content is still loading.
 */
function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    frame: false,
    backgroundColor: '#FAFAFA',
    title: 'Gesture Control',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, '..', 'src', 'index.html'));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Window controls for the frameless window (buttons live in the renderer,
// they reach us only through the preload API).
ipcMain.on('window:minimize', () => {
  if (mainWindow) mainWindow.minimize();
});

ipcMain.on('window:maximize', () => {
  if (!mainWindow) return;
  if (mainWindow.isMaximized()) mainWindow.unmaximize();
  else mainWindow.maximize();
});

ipcMain.on('window:close', () => {
  if (mainWindow) mainWindow.close();
});

app.whenReady().then(() => {
  createMainWindow();

  app.on('activate', () => {
    // macOS convention: recreate window on dock click if all are closed.
    if (BrowserWindow.getAllWindows().length === 0) createMainWindow();
  });
});

app.on('window-all-closed', () => {
  // macOS convention: app stays in the dock until Cmd+Q.
  if (process.platform !== 'darwin') app.quit();
});
