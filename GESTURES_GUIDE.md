# 🖐️ Hand Gesture Controls Guide

## All Available Gestures

### 🎮 Basic Controls

| Gesture | Fingers | Symbol | Action | Description |
|---------|---------|--------|--------|-------------|
| **Closed Fist** | 0-1 | ✊ | **PLAY** | Start/Resume video playback |
| **Open Palm** | 5 | 👋 | **PAUSE** | Pause video playback |
| **Peace Sign** | 2 | ✌️ | **REWIND** | Go back 10 seconds |
| **Three Fingers** | 3 | 🤟 | **FORWARD** | Skip ahead 10 seconds |
| **Four Fingers** | 4 | 🖖 | **SHUTDOWN** | Shutdown Mac system |

---

## 📋 Detailed Gesture Instructions

### 1. ✊ Closed Fist - PLAY
- **Finger Count**: 0-1 fingers extended
- **Action**: Play/Resume video
- **How to do it**: 
  - Close all fingers into a tight fist
  - Tuck thumb inside or keep it closed
  - Hold steady for 8 frames (~0.27 seconds)
- **Use when**: Video is paused and you want to start playing

### 2. 👋 Open Palm - PAUSE
- **Finger Count**: 5 fingers extended
- **Action**: Pause video
- **How to do it**:
  - Spread all 5 fingers wide and straight
  - Face palm directly toward camera
  - Keep hand steady for 12 frames
- **Use when**: Video is playing and you want to pause

### 3. ✌️ Peace Sign - REWIND 10 SECONDS
- **Finger Count**: 2 fingers extended
- **Action**: Skip backward 10 seconds
- **How to do it**:
  - Extend index and middle fingers (like peace sign)
  - Keep other fingers closed
  - Hold steady for 8 frames
- **Use when**: You want to replay recent content
- **Keyboard equivalent**: Left arrow key

### 4. 🤟 Three Fingers - FORWARD 10 SECONDS
- **Finger Count**: 3 fingers extended
- **Action**: Skip forward 10 seconds
- **How to do it**:
  - Extend index, middle, and ring fingers
  - Keep pinky and thumb closed
  - Hold steady for 12 frames
- **Use when**: You want to skip ahead in the video
- **Keyboard equivalent**: Right arrow key

### 5. 🖖 Four Fingers - SHUTDOWN MAC
- **Finger Count**: 4 fingers extended (no thumb)
- **Action**: Shutdown your Mac computer
- **How to do it**:
  - Extend all four fingers (index, middle, ring, pinky)
  - Keep thumb folded/closed
  - Hold steady for 12 frames
- **Use when**: You want to shut down your Mac
- **Warning**: This will initiate system shutdown - use carefully!
- **System command**: Uses AppleScript shutdown dialog

---

## 💡 Tips for Best Detection

### Hand Position
- Keep your hand **1-2 feet** from the camera
- Face **palm directly** toward camera
- **Entire hand** should be visible in frame
- Use **contrasting background** (dark hand on light background or vice versa)

### Lighting
- Ensure **good, even lighting** on your hand
- Avoid backlighting (don't have a bright window behind you)
- Front lighting or overhead lighting works best

### Gesture Execution
- Hold each gesture **steady** for at least 12 frames (~0.4 seconds)
- Watch the **"Stability"** counter on screen (needs to reach 12/12)
- Don't move your hand while performing gesture
- Wait for **confirmation message** before changing gesture

### Common Issues
❌ **Moving hand while gesturing** → Resets stability counter
❌ **Partially closed fingers** → May miscount fingers
❌ **Tilted or angled hand** → Harder to detect accurately
❌ **Hand too close/far from camera** → Detection issues

✅ **Keep hand steady**
✅ **Make clear, deliberate gestures**
✅ **Wait for confirmation**
✅ **Ensure good lighting**

---

## 🎯 Supported Media Players

These gestures work with any media player that responds to keyboard shortcuts:

### Web Browsers
- ✅ YouTube
- ✅ Netflix
- ✅ Amazon Prime Video
- ✅ Disney+
- ✅ Vimeo
- ✅ Twitch
- ✅ Dailymotion

### Desktop Applications
- ✅ VLC Media Player
- ✅ QuickTime Player (macOS)
- ✅ Windows Media Player
- ✅ Spotify
- ✅ Apple Music
- ✅ iTunes
- ✅ Potplayer
- ✅ MPC-HC

---

## ⚙️ Technical Details

### Keyboard Shortcuts Used
- **PLAY/PAUSE**: Space bar
- **REWIND**: Left arrow (← 10 seconds back)
- **FORWARD**: Right arrow (→ 10 seconds ahead)

### Detection Parameters
- **Stability Threshold**: 8 consecutive frames
- **Frame Rate**: ~30 FPS
- **Detection Time**: ~0.27 seconds
- **Cooldown**: 2.5 seconds between commands
- **Hand Landmarks**: 21 points detected per hand

### Gesture Classification
```
finger_count >= 4  → OPEN_PALM (PAUSE)
finger_count <= 1  → CLOSED_FIST (PLAY)
finger_count == 2  → PEACE_SIGN (REWIND)
finger_count == 3  → THREE_FINGERS (FORWARD)
```

---

## 🎓 Quick Start

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Position yourself**
   - Sit 1-2 feet from camera
   - Ensure good lighting
   - Make sure entire hand is visible

3. **Test gestures**
   - Start with **closed fist** → Should see "PLAY ▶"
   - Try **open palm** → Should see "PAUSE ⏸"
   - Show **peace sign** → Should see "REWIND ⏪"
   - Show **three fingers** → Should see "FORWARD ⏩"

4. **Control your media**
   - Open YouTube or any video player
   - Click on the player window (give it focus)
   - Use gestures to control playback!

---

## 📊 Gesture Practice Chart

Practice making these gestures clearly:

```
✊ Fist (PLAY)           👋 Palm (PAUSE)
   0-1 fingers              4-5 fingers
   
     ____                    _____
    |    |                  / | | \
    |____|                 |  | | |
                           |  | | |
                           |  | | |

✌️ Peace (REWIND)       🤟 Three (FORWARD)  
   2 fingers                3 fingers
   
     | |                     | | |
     | |                     | | |
     | |                     | | |
    |___|                   |_____|
```

---

## 🔧 Customization

Want different time intervals? Edit `media_controller.py`:

```python
# For 5-second skip instead of 10:
def skip_forward(self):
    pyautogui.press('right')  # YouTube: 5 seconds with single arrow
    # Or press twice for 10 seconds:
    # pyautogui.press('right')
    # pyautogui.press('right')
```

For YouTube specifically:
- `j` key = 10 seconds backward
- `l` key = 10 seconds forward
- Left arrow = 5 seconds backward
- Right arrow = 5 seconds forward

---

## ❓ FAQ

**Q: Can I add more gestures?**
A: Yes! Edit `hand_detector.py` to add custom finger count patterns.

**Q: Why 8 frames stability?**
A: Prevents accidental triggers. Adjustable in `main.py` (stability_threshold).

**Q: Do gestures work simultaneously?**
A: No, one gesture at a time. 2.5 second cooldown between commands.

**Q: Can I use with two hands?**
A: Currently single hand only. Multi-hand support can be added.

**Q: What if gestures aren't detected?**
A: Check lighting, hand position, and ensure fingers are clearly extended/closed.

---

## 🎉 Happy Gesturing!

Master these four gestures and you'll have complete touchless control over your media playback!

**Remember**: 
- ✊ Fist = Play
- 👋 Palm = Pause  
- ✌️ Two = Rewind
- 🤟 Three = Forward

Press 'Q' to quit anytime!
