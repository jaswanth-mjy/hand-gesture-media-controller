# 🎬 Hand Gesture Media Controller

[![GitHub Stars](https://img.shields.io/github/stars/jaswanth-mjy/hand-gesture-media-controller?style=social)](https://github.com/jaswanth-mjy/hand-gesture-media-controller/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/jaswanth-mjy/hand-gesture-media-controller?style=social)](https://github.com/jaswanth-mjy/hand-gesture-media-controller/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/jaswanth-mjy/hand-gesture-media-controller)](https://github.com/jaswanth-mjy/hand-gesture-media-controller/issues)
[![GitHub License](https://img.shields.io/github/license/jaswanth-mjy/hand-gesture-media-controller)](https://github.com/jaswanth-mjy/hand-gesture-media-controller/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

A computer vision application that controls media playback (videos, music, streaming) using hand gestures detected through your webcam. Simply show your hand to the camera to play or pause any media on your laptop!

🔗 **[View Demo](https://github.com/jaswanth-mjy/hand-gesture-media-controller)** | 📖 **[Documentation](https://github.com/jaswanth-mjy/hand-gesture-media-controller#readme)** | 🐛 **[Report Bug](https://github.com/jaswanth-mjy/hand-gesture-media-controller/issues)** | ✨ **[Request Feature](https://github.com/jaswanth-mjy/hand-gesture-media-controller/issues)**

## ✨ Features

- **✊ Closed Fist (0-1 fingers extended)** → PLAY media
- **🖐️ Open Palm (5 fingers extended)** → PAUSE media
- **✌️ Peace Sign (2 fingers)** → REWIND 10 seconds
- **🤟 Three Fingers** → FORWARD 10 seconds
- **🖖 Four Fingers** → SHUTDOWN Mac
- **Universal Control**: Works with YouTube, Netflix, Spotify, VLC, QuickTime, and any media player
- **Smart Detection**: Only sends commands when state needs to change (won't pause if already paused)
- **Stable Recognition**: Requires 12 consecutive frames to confirm gesture (prevents false triggers)
- **Visual Feedback**: Real-time display of detected fingers, gesture, and media state
- **Cross-platform**: Works on macOS, Windows, and Linux

## 🎯 How It Works

The application uses three main technologies:

1. **OpenCV (cv2)** - Captures video from webcam and processes frames in real-time
2. **MediaPipe** - Detects 21 hand landmarks to identify finger positions and count extended fingers
3. **PyAutoGUI** - Sends keyboard commands (space bar) to control media playback

### Technical Architecture

```
Webcam → OpenCV → MediaPipe Hand Detection → Finger Counting → Gesture Recognition → Command Execution
```

**Process Flow:**
1. Camera captures video frames at 30 FPS
2. Each frame is analyzed by MediaPipe to detect hand landmarks
3. Algorithm counts extended fingers by comparing fingertip positions with joint positions
4. Gesture is classified: 5 fingers = OPEN_PALM, 0-1 fingers = CLOSED_FIST, 2 = PEACE_SIGN, 3 = THREE_FINGERS, 4 = FOUR_FINGERS
5. If gesture is stable for 12 frames (0.4 seconds), command is executed
6. PyAutoGUI sends keyboard commands (space, arrows, or shutdown) to control the system
7. System tracks state to prevent duplicate commands

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam/Camera
- macOS, Windows, or Linux

## 🚀 Installation

### Option 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/jaswanth-mjy/hand-gesture-media-controller.git

# Navigate to project directory
cd hand-gesture-media-controller

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Manual Setup

### 1. Clone or Download the Project

```bash
cd "/Users/mjaswanth/pause or play"
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `opencv-python` - Computer vision library
- `mediapipe` - Hand detection and tracking
- `pyautogui` - Keyboard automation
- `numpy` - Numerical operations

## 🎮 Usage

### 1. Start the Application

```bash
python main.py
```

### 2. Grant Camera Permissions

On macOS, you may need to grant camera access:
- Go to **System Preferences** → **Security & Privacy** → **Camera**
- Allow access for Terminal or your Python interpreter

### 3. Control Your Media

1. **Open your media player** (YouTube in browser, VLC, Spotify, etc.)
2. **Position yourself** in front of the camera
3. **Show gestures:**
   - ✊ **Closed fist** (make a fist) → PLAY
   - 🖐️ **Open palm** (spread all 5 fingers) → PAUSE
   - ✌️ **Peace sign** (2 fingers) → REWIND 10 seconds
   - 🤟 **Three fingers** → FORWARD 10 seconds
   - 🖖 **Four fingers** (no thumb) → SHUTDOWN Mac
4. Press **'Q'** to quit the application

## 📱 Supported Applications

The application works with virtually any media player because it sends the universal "space bar" command:

### Browsers
- ✅ YouTube
- ✅ Netflix
- ✅ Amazon Prime Video
- ✅ Disney+
- ✅ Vimeo
- ✅ Twitch

### Desktop Applications
- ✅ VLC Media Player
- ✅ QuickTime Player (macOS)
- ✅ Windows Media Player
- ✅ Spotify
- ✅ Apple Music
- ✅ iTunes
- ✅ And many more!

## 🛠️ Configuration

You can adjust settings in the code:

### Hand Detection Sensitivity

In `main.py`, modify the `HandDetector` initialization:

```python
detector = HandDetector(
    max_hands=1,                    # Number of hands to detect
    detection_confidence=0.7,        # 0.0 to 1.0 (higher = more strict)
    tracking_confidence=0.7          # 0.0 to 1.0 (higher = more stable)
)
```

### Command Cooldown

In `main.py`, adjust the cooldown between commands:

```python
controller = MediaController(cooldown=1.5)  # Seconds between commands
```

### Gesture Stability

In `main.py`, change how many consecutive frames confirm a gesture:

```python
stability_threshold = 3  # Number of frames (higher = more stable, slower response)
```

## 🐛 Troubleshooting

### Camera Not Working

**Problem:** "Could not open webcam" error

**Solutions:**
- Check if another application is using the camera (Zoom, Skype, etc.)
- Grant camera permissions to Terminal/Python:
  - **macOS:** System Preferences → Security & Privacy → Camera
  - **Windows:** Settings → Privacy → Camera
- Try different camera index: Change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in `main.py`
- Verify camera works in other apps first

### Hand Not Detected

**Problem:** "NO HAND DETECTED" message persists

**Solutions:**
- **Lighting:** Ensure good, even lighting on your hand
- **Distance:** Position hand 1-2 feet from camera
- **Background:** Use contrasting background (dark hand on light background or vice versa)
- **Hand visibility:** Keep entire hand within camera frame
- **Lower detection threshold:** Edit `main.py` line 40:
  ```python
  detector = HandDetector(max_hands=1, detection_confidence=0.5, tracking_confidence=0.5)
  ```

### Commands Not Working

**Problem:** Gestures detected but media doesn't play/pause

**Solutions:**

1. **Give Media Player Focus:**
   - Click on the media player window before showing gestures
   - The active window receives keyboard commands

2. **Test Space Bar Manually:**
   - Click on media player
   - Press space bar on keyboard
   - If it doesn't work, the app won't work either

3. **macOS Accessibility Permissions:**
   - Open **System Preferences** → **Security & Privacy** → **Accessibility**
   - Click lock icon to make changes
   - Add **Terminal** (or your Python application) to allowed apps
   - This lets PyAutoGUI send keyboard commands

4. **Browser Issues:**
   - Some browsers block keyboard automation
   - Try fullscreen mode (F key on YouTube)
   - Ensure media player controls are visible

5. **Check Cooldown:**
   - Commands are limited to once every 2.5 seconds
   - Wait between gestures

### Wrong Gesture Detected

**Problem:** Fist detected as open palm or vice versa

**Solutions:**

1. **Check Detection Display:**
   - Look at terminal output: shows finger count
   - Open palm should show 4-5 fingers
   - Closed fist should show 0-1 fingers

2. **Make Clear Gestures:**
   - **Open Palm:** Spread ALL fingers wide and straight
   - **Closed Fist:** Curl ALL fingers tightly, tuck thumb in

3. **Adjust Detection Threshold:**
   - Edit `hand_detector.py` line 112:
   ```python
   if tip_y < pip_y - 30:  # Increase from 20 to 30 for stricter detection
   ```

4. **Camera Angle:**
   - Face palm directly toward camera
   - Avoid tilted or sideways angles

### Commands Repeating/Fluctuating

**Problem:** Video keeps playing and pausing rapidly

**Solutions:**

1. **Current Settings (Already Implemented):**
   - Stability threshold: 8 frames (~0.27 sec)
   - Cooldown: 2.5 seconds between commands
   - Command executes once per gesture

2. **If Still Having Issues:**
   - Increase `stability_threshold` in `main.py` line 54:
   ```python
   stability_threshold = 12  # Increase from 8 to 12
   ```
   - Increase `cooldown` in `main.py` line 41:
   ```python
   controller = MediaController(cooldown=3.0)  # Increase from 2.5 to 3.0
   ```

3. **Hold Gesture Steady:**
   - Keep hand still for full 8 frames
   - Watch stability counter: "Stable: X/8"
   - Don't move hand until command executes

### Performance Issues

**Problem:** Application is slow or laggy

**Solutions:**
- Close other camera applications
- Reduce camera resolution in `main.py` line 29:
  ```python
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  ```
- Close unnecessary background applications
- Check CPU usage - MediaPipe is computationally intensive

## 📁 Project Structure

```
pause or play/
├── main.py                 # Main application entry point and control loop
├── hand_detector.py        # Hand detection and gesture recognition module
├── media_controller.py     # Media playback control via keyboard automation
├── requirements.txt        # Python dependencies list
├── .gitignore             # Git ignore patterns
└── README.md              # Complete project documentation
```

## 🔧 Technical Details

### Module Breakdown

#### 1. `hand_detector.py` - Hand Detection Module

**Purpose:** Detects hands in video frames and counts extended fingers

**Key Components:**
- `HandDetector` class wraps MediaPipe Hands solution
- `find_hands()` - Processes frame and detects hand landmarks (21 points per hand)
- `get_finger_positions()` - Extracts pixel coordinates of all landmarks
- `count_fingers()` - Counts extended fingers using landmark comparison
- `detect_gesture()` - Classifies gesture as OPEN_PALM, CLOSED_FIST, or UNKNOWN

**Finger Counting Algorithm:**
- **Thumb:** Compares tip (landmark 4) distance from MCP (landmark 2) with IP joint (landmark 3)
  - Extended if tip is further from MCP than IP is
- **Other 4 Fingers:** Compares fingertip with PIP joint
  - Index finger: tip (landmark 8) vs PIP (landmark 6)
  - Middle finger: tip (landmark 12) vs PIP (landmark 10)
  - Ring finger: tip (landmark 16) vs PIP (landmark 14)
  - Pinky: tip (landmark 20) vs PIP (landmark 18)
  - Extended if tip Y-coordinate is 20+ pixels above PIP

**Gesture Classification:**
- `finger_count >= 4` → OPEN_PALM (play video)
- `finger_count <= 1` → CLOSED_FIST (pause video)
- `finger_count == 2 or 3` → UNKNOWN (no action)

#### 2. `media_controller.py` - Media Control Module

**Purpose:** Sends keyboard commands to control media playback

**Key Components:**
- `MediaController` class manages command execution and state tracking
- `can_execute_command()` - Enforces 2.5 second cooldown between commands
- `play()` - Sends space bar press to play media (only if not already playing)
- `pause()` - Sends space bar press to pause media (only if not already paused)

**State Management:**
- Tracks current state: "PLAYING", "PAUSED", or None
- Prevents duplicate commands (won't pause if already paused)
- Cooldown timer prevents rapid command toggling

**Why Space Bar?**
Space bar is the universal play/pause shortcut for:
- All web browsers (YouTube, Netflix, etc.)
- VLC, QuickTime, Windows Media Player
- Spotify, Apple Music, iTunes
- Most other media applications

#### 3. `main.py` - Main Application

**Purpose:** Orchestrates the entire system and handles user interaction

**Key Components:**

**Initialization:**
```python
cap = cv2.VideoCapture(0)  # Open webcam
detector = HandDetector()   # Initialize hand detector
controller = MediaController(cooldown=2.5)  # Initialize media controller
```

**Main Loop Process:**
1. Capture frame from webcam
2. Flip frame horizontally (mirror view)
3. Detect hand gesture and count fingers
4. Track gesture stability (must be stable for 8 consecutive frames)
5. Execute command only when:
   - Gesture has been stable for 8 frames
   - Command hasn't been executed for this gesture yet
   - Media state needs to change (play when paused, pause when playing)
6. Display visual feedback on frame
7. Show frame in window
8. Wait for 'Q' key to quit

**Stability System:**
- `stability_threshold = 8` - Requires 8 consecutive frames of same gesture
- Prevents false positives from hand movements
- Ensures deliberate gesture detection
- At 30 FPS, this is ~0.27 seconds

**State Tracking:**
- `last_gesture` - Previous frame's gesture
- `gesture_stable_frames` - Counter for consecutive matching frames
- `command_executed_for_current_gesture` - Flag to prevent command repetition
- Resets when gesture changes

### How Finger Detection Works

**MediaPipe Hand Landmarks:**
MediaPipe detects 21 landmarks on each hand:
- 0: Wrist
- 1-4: Thumb (CMC, MCP, IP, TIP)
- 5-8: Index finger (MCP, PIP, DIP, TIP)
- 9-12: Middle finger (MCP, PIP, DIP, TIP)
- 13-16: Ring finger (MCP, PIP, DIP, TIP)
- 17-20: Pinky (MCP, PIP, DIP, TIP)

**Detection Logic:**
```
For each finger:
  - Get fingertip Y coordinate
  - Get PIP joint Y coordinate
  - If (tip_y < pip_y - 20 pixels):
      Finger is EXTENDED
  - Else:
      Finger is CLOSED
```

**Why This Works:**
- Y coordinates increase downward in images
- Extended fingers have tips ABOVE (lower Y) their joints
- 20-pixel threshold prevents false positives from slightly bent fingers

### Command Execution Logic

```python
if gesture_stable_frames >= 8 and not command_executed_for_current_gesture:
    if gesture == "OPEN_PALM" and current_state != "PLAYING":
        send_play_command()
    elif gesture == "CLOSED_FIST" and current_state != "PAUSED":
        send_pause_command()
```

**Key Design Decisions:**
1. **State checking** prevents sending PLAY when already playing
2. **Stability requirement** prevents accidental triggers
3. **Execution flag** prevents command repetition for same gesture
4. **Cooldown timer** prevents rapid toggling
5. **Gesture change detection** allows new command only after different gesture

## 🎨 Advanced Customization

### Adjusting Detection Sensitivity

**Make finger detection stricter (fewer false positives):**

In `hand_detector.py`, line 112:
```python
if tip_y < pip_y - 30:  # Increase from 20 to 30 or 40
```

**Make finger detection more lenient (detect bent fingers):**
```python
if tip_y < pip_y - 10:  # Decrease from 20 to 10 or 5
```

### Changing Gesture Classification

In `hand_detector.py`, lines 137-142:
```python
# Current settings:
if finger_count >= 4:  # Open palm
    gesture = "OPEN_PALM"
elif finger_count <= 1:  # Closed fist
    gesture = "CLOSED_FIST"

# Make it more strict (require exact counts):
if finger_count == 5:  # Must be exactly 5
    gesture = "OPEN_PALM"
elif finger_count == 0:  # Must be exactly 0
    gesture = "CLOSED_FIST"
```

### Adjusting Stability and Cooldown

In `main.py`:

**Line 54 - Stability Threshold:**
```python
stability_threshold = 8  # Current: 8 frames (~0.27 sec)
# Lower = faster response, more false positives
# Higher = slower response, fewer false positives
# Try: 5 (fast), 12 (very stable), 15 (ultra stable)
```

**Line 41 - Cooldown Period:**
```python
controller = MediaController(cooldown=2.5)  # Current: 2.5 seconds
# Lower = faster repeated commands
# Higher = slower repeated commands
# Try: 1.5 (fast), 3.0 (slow), 5.0 (very slow)
```

### Adding New Gestures

Want to add volume control or other gestures? Here's the framework:

In `hand_detector.py`, add to `detect_gesture()`:
```python
def detect_gesture(self, img):
    # ... existing code ...
    
    if finger_count >= 4:
        gesture = "OPEN_PALM"
    elif finger_count <= 1:
        gesture = "CLOSED_FIST"
    elif finger_count == 2:  # Peace sign
        gesture = "PEACE_SIGN"
    elif finger_count == 3:  # Three fingers
        gesture = "THREE_FINGERS"
    else:
        gesture = "UNKNOWN"
    
    return gesture, finger_count, img
```

In `main.py`, add command handling:
```python
if gesture == "PEACE_SIGN":
    # Add your custom command here
    pyautogui.press('volumeup')
```

### Changing Keyboard Shortcuts

In `media_controller.py`, change the key press:

```python
# Current: Space bar (play/pause)
pyautogui.press('space')

# Other options:
pyautogui.press('k')           # YouTube play/pause
pyautogui.press('right')       # Skip forward
pyautogui.press('left')        # Skip backward
pyautogui.press('volumeup')    # Increase volume
pyautogui.press('volumedown')  # Decrease volume
pyautogui.press('f')           # Toggle fullscreen
pyautogui.press('m')           # Mute/unmute
```

## ⚠️ Important Notes

### System Requirements
- **Minimum:** 2GB RAM, dual-core CPU, webcam
- **Recommended:** 4GB+ RAM, quad-core CPU, HD webcam
- **Python:** Version 3.8 or higher

### Permissions Required
1. **Camera Access:** App needs webcam access to detect hand gestures
2. **Accessibility (macOS):** Required for PyAutoGUI to send keyboard commands
3. **Focus:** Media player window must be active to receive commands

### Privacy & Security
- ✅ **100% Local Processing** - All detection happens on your device
- ✅ **No Network Access** - Application doesn't connect to internet
- ✅ **No Data Storage** - Video frames are processed in real-time and discarded
- ✅ **Open Source** - All code is visible and auditable

### Performance Tips
- Close other camera applications (Zoom, Skype, etc.)
- Use good lighting for better detection
- Position camera at eye level for best results
- Run on battery power may reduce FPS

## 🚀 Future Enhancement Ideas

1. **Multiple Gestures:**
   - Thumbs up/down for volume
   - Swipe left/right for skip
   - Pinch for zoom
   - Wave for next track

2. **Two-Hand Gestures:**
   - Clap for pause/play
   - Hands apart for volume
   - Hands together for mute

3. **Configuration GUI:**
   - Adjust settings without editing code
   - Save/load presets
   - Test gestures in real-time

4. **Application Profiles:**
   - Different gestures for different apps
   - Auto-detect active media player
   - Custom shortcuts per application

5. **Machine Learning:**
   - Train custom gesture recognizer
   - Learn user's hand patterns
   - Adaptive thresholds

## 📊 Project Statistics

- **Lines of Code:** ~500
- **Number of Files:** 5
- **Dependencies:** 4 (OpenCV, MediaPipe, PyAutoGUI, NumPy)
- **Supported Gestures:** 2 (Open Palm, Closed Fist)
- **Supported Platforms:** 3 (macOS, Windows, Linux)
- **Detection Points:** 21 hand landmarks
- **Frame Rate:** ~30 FPS
- **Detection Latency:** ~0.27 seconds (8 frames at 30 FPS)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs:** Open an issue with detailed description
2. **Suggest Features:** Share your ideas for improvements
3. **Submit Pull Requests:** Add new features or fix bugs
4. **Improve Documentation:** Help clarify setup or usage
5. **Share Results:** Post videos or screenshots of your setup

## 📄 License

This project is open-source and available for:
- ✅ Personal use
- ✅ Educational purposes
- ✅ Research and development
- ✅ Commercial use with attribution

## 🙏 Acknowledgments

**Technologies Used:**
- **[MediaPipe](https://mediapipe.dev/)** by Google - Real-time hand tracking
- **[OpenCV](https://opencv.org/)** - Computer vision and image processing
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)** - Cross-platform keyboard automation
- **[NumPy](https://numpy.org/)** - Numerical computing

**Inspiration:**
- Computer vision research in human-computer interaction
- Touchless control systems for accessibility
- Gesture-based user interfaces

## 📧 Contact & Support

- **Issues:** Use GitHub Issues for bug reports
- **Questions:** Check troubleshooting section first
- **Feedback:** Share your experience and suggestions

---

## 🎯 Quick Start Summary

1. **Install:** `pip install -r requirements.txt`
2. **Run:** `python main.py`
3. **Use:** Show open palm to play, closed fist to pause
4. **Exit:** Press 'Q' key

**That's it! Enjoy hands-free media control! 🎉**

---

*Built with ❤️ using Computer Vision and Python*
