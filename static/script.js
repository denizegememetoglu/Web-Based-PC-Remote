const trackpad = document.getElementById('trackpad');
let lastX = 0;
let lastY = 0;
let isTouching = false;

// --- Trackpad Logic ---
trackpad.addEventListener('touchstart', (e) => {
    e.preventDefault(); // Stop the browser from zooming/scrolling
    const touch = e.touches[0];
    lastX = touch.clientX;
    lastY = touch.clientY;
    isTouching = true;
});

trackpad.addEventListener('touchmove', (e) => {
    e.preventDefault();
    if (!isTouching) return;

    const touch = e.touches[0];
    const dx = touch.clientX - lastX;
    const dy = touch.clientY - lastY;

    // Send the move to the PC!
    // We send raw deltas; the server handles the actual movement using PyAutoGUI.
    fetch('/api/mouse/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        // Multiplier 1.5 feels about right for sensitivity. Adjust if it feels sluggish.
        body: JSON.stringify({dx: dx * 1.5, dy: dy * 1.5}) 
    });

    lastX = touch.clientX;
    lastY = touch.clientY;
});

trackpad.addEventListener('touchend', (e) => {
    isTouching = false;
});


// --- Controls ---

function sendMedia(action) {
    // Mapping 'next' and 'prev' logic to seek arrows for better utility
    if (action === 'prev') action = 'seekbackward';
    if (action === 'next') action = 'seekforward';
    fetch(`/api/media/${action}`, {method: 'POST'});
}

function updateVolume(value) {
    // Sending the exact slide value to the server
    fetch('/api/volume/set', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({level: value})
    });
}

function toggleMute() {
    // Just a simple toggle
    fetch('/api/volume/mute', {method: 'POST'});
}

function sendClick(button) {
    fetch('/api/mouse/click', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({button: button})
    });
}

function sendScroll(dy) {
    fetch('/api/mouse/scroll', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({dy: dy * 100}) // Scroll amount
    });
}
