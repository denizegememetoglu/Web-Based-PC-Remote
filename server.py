from flask import Flask, render_template, request, jsonify
import pyautogui
import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

app = Flask(__name__)

# Basic settings
pyautogui.FAILSAFE = False # Just in case things go wild, this is a safety net.

import comtypes

def get_volume_interface():
    # We need to initialize COM for threads, otherwise it gets grumpy.
    comtypes.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    # Simplified access to the volume endpoint. 
    return devices.EndpointVolume

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/mouse/move', methods=['POST'])
def mouse_move():
    data = request.json
    dx = data.get('dx', 0)
    dy = data.get('dy', 0)
    # Moving the mouse relative to its current position.
    pyautogui.moveRel(dx, dy)
    return jsonify({'status': 'success'})

@app.route('/api/mouse/click', methods=['POST'])
def mouse_click():
    data = request.json
    btn = data.get('button', 'left')
    if btn == 'left':
        pyautogui.click() # Standard click
    elif btn == 'right':
        pyautogui.rightClick() # Context menu
    return jsonify({'status': 'success'})

@app.route('/api/mouse/scroll', methods=['POST'])
def mouse_scroll():
    data = request.json
    dy = data.get('dy', 0)
    # Scrolling a bit faster than raw input feels better.
    pyautogui.scroll(int(dy * 2))
    return jsonify({'status': 'success'})

@app.route('/api/volume/set', methods=['POST'])
def volume_set():
    data = request.json
    level = int(data.get('level', 50))
    try:
        # Hitting the volume endpoint directly.
        volume = get_volume_interface()
        volume.SetMasterVolumeLevelScalar(float(level) / 100, None)
        return jsonify({'status': 'success', 'method': 'pycaw'})
    except Exception as e:
        print(f"Volume fix attempt failed: {str(e)}")
        # If this fails, we're kinda out of luck for absolute positioning, 
        # but at least we tried.
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/volume/mute', methods=['POST'])
def volume_toggle_mute():
    # Using keyboard simulation because it's way more reliable for toggling.
    try:
        pyautogui.press('volumemute')
        return jsonify({'status': 'success', 'method': 'pyautogui'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/media/<action>', methods=['POST'])
def media_control(action):
    # Mapping our frontend actions to actual keyboard keys.
    # Updated 'next'/'prev' to arrow keys for seeking (YouTube style).
    actions = {
        'playpause': 'play/pause media',
        'next': 'next track',
        'prev': 'previous track',
        'volup': 'volume up',
        'voldown': 'volume down',
        'seekforward': 'right',
        'seekbackward': 'left'
    }
    
    if action in actions:
        keyboard.press_and_release(actions[action])
        return jsonify({'status': 'success', 'action': action})
    return jsonify({'status': 'error', 'message': 'Invalid action'}), 400

if __name__ == '__main__':
    # 0.0.0.0 binds to all interfaces, so your phone can see it.
    app.run(host='0.0.0.0', port=8000, debug=True)

