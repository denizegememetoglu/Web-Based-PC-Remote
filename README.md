# 📱 Web-Based PC Remote

Hey! This is a little project I whipped up to control my Windows PC from my phone without installing any sketchy apps. It's basically a web server running on your PC that you open in your phone's browser. Super simple.

![UI Preview](preview.png)

## ✨ What can it do?

- **🖱️ Mouse/Trackpad**: Touch your phone screen to move the mouse. It's surprisingly smooth.
- **🔊 Volume**: Slider for that perfect volume level, plus a Mute button for when things get loud.
- **⏯️ Media**: Play/Pause basically anything.
- **⏩ Seek**: I mapped the "Next/Prev" buttons to Arrow Keys, so you can skip through YouTube or movies easily.

## 🚀 How to use it?

### Setup

1.  Make sure you have **Python** installed.
2.  Clone this repo (or just download the zip).
    ```bash
    git clone https://github.com/yourusername/pc-remote-control.git
    cd pc-remote-control
    ```
3.  Install the libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Running it

1.  Run the server:
    ```bash
    python server.py
    ```
2.  Your firewall might pop up asking for permission—allow it so your phone can see the server.

3.  Find your local IP (CMD > `ipconfig`) and go to `http://YOUR_IP:8000` on your phone.

That's it. No login, no cloud, just local network magic.

## 🛠️ Tech Stack

Just Python (Flask) doing the heavy lifting with `pyautogui` and `pycaw`. Frontend is vanilla HTML/CSS/JS because frameworks are overkill for this.

## 📝 License

Do whatever you want with it! standard MIT license.
