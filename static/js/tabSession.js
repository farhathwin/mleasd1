// tabSession.js

// Function to generate a unique ID
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Function to generate a unique tab ID
function generateTabId() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

// Get the tab ID from localStorage or create a new one
let tabId = localStorage.getItem('tabId');
if (!tabId) {
    tabId = generateTabId();
    localStorage.setItem('tabId', tabId);
}

// Set the tab ID in a hidden input field
window.addEventListener('DOMContentLoaded', (event) => {
    let tabIdInput = document.getElementById('tabId');
    if (tabIdInput) {
        tabIdInput.value = tabId;
    }
});

window.onload = setTabId;
