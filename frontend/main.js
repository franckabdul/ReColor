const { app, BrowserWindow, Menu, ipcMain } = require("electron");
const path = require('path');
const fs = require('fs');

async function createWindow() {
  // Dynamically import electron-is-dev
  const { default: isDev } = await import('electron-is-dev');

  const win = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Ensure you have a preload.js for contextBridge
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
    },
  });

  win.loadFile("HTML/index.html");

  // Remove the default menu
  Menu.setApplicationMenu(null);

  // You can now use isDev here if needed
  console.log('Is development mode:', isDev);
}

// Initialize config directory and file
function initializeConfig() {
  const userDataPath = app.getPath('userData');
  const configDir = path.join(userDataPath, 'config');
  const configFile = path.join(configDir, 'config.json');

  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }

  if (!fs.existsSync(configFile)) {
    const defaultConfig = { serverUrl: 'http://127.0.0.1:5000' };
    fs.writeFileSync(configFile, JSON.stringify(defaultConfig, null, 2), 'utf-8');
  }
}

// Handle IPC communication
ipcMain.handle('getConfig', () => {
  try {
    const userDataPath = app.getPath('userData');
    const configFile = path.join(userDataPath, 'config', 'config.json');
    const config = JSON.parse(fs.readFileSync(configFile, 'utf-8'));
    return config;
  } catch (error) {
    console.error("Failed to read configuration:", error);
    return { error: 'Failed to load configuration' };
  }
});

ipcMain.handle('updateConfig', (event, newConfig) => {
  try {
    const userDataPath = app.getPath('userData');
    const configFile = path.join(userDataPath, 'config', 'config.json');
    fs.writeFileSync(configFile, JSON.stringify(newConfig, null, 2), 'utf-8');
    return { success: true };
  } catch (error) {
    console.error("Failed to update configuration:", error);
    return { error: 'Failed to update configuration' };
  }
});

app.whenReady().then(() => {
  initializeConfig(); // Ensure config is initialized before creating the window
  createWindow();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
