const { contextBridge, ipcRenderer } = require('electron');

// Safely expose certain Node.js features to the renderer process
contextBridge.exposeInMainWorld('electron', {
    versions: {
        node: () => process.versions.node,
        chrome: () => process.versions.chrome,
        electron: () => process.versions.electron,
    },
    sendMessage: (channel, data) => ipcRenderer.send(channel, data),
    onReceiveMessage: (channel, callback) => ipcRenderer.on(channel, (event, ...args) => callback(...args)),
    invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args) // Added IPC invoke method
});

// DOM manipulation to replace version info
window.addEventListener('DOMContentLoaded', () => {
    // Function to replace text in a given DOM element
    const replaceText = (selector, text) => {
        const element = document.getElementById(selector);
        if (element) element.innerText = text;
    };

    // Update version info in the DOM
    for (const type of ['chrome', 'node', 'electron']) {
        replaceText(`${type}-version`, process.versions[type]);
    }
});
