const path = require('node:path');
const { app, BrowserWindow } = require('electron');

/**
 * Create the main application window.
 * Frameless (frame: false) + solid background so the window looks clean
 * while the web content is still loading.
 */
function createMainWindow() {
  const win = new BrowserWindow({
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

  win.loadFile(path.join(__dirname, '..', 'src', 'index.html'));
}

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
