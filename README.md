# 🎮 Subway Surfers Gesture Controller

Control **Subway Surfers** (or any similar game) using your **hands and body** through your webcam — no keyboard needed!

Two control modes are available:
- ✋ **Finger Gesture Mode** — count fingers to trigger actions
- 🧍 **Full Body Pose Mode** — lean left/right, jump, and crouch with your whole body

---

## 📹 Demo Video

👉 [Watch the Demo on Google Drive](https://drive.google.com/file/d/13UNUDpWrGPRnp1SAysGknnOlasbgxPug/view?usp=drivesdkimport)

---

## 📁 Project Structure

```
subway-surfers-gesture-control/
│
├── main.py                    # CLI launcher (choose mode via terminal)
├── gui_control.py             # GUI launcher (buttons interface)
├── finger_gesture_control.py  # Finger counting gesture logic
├── pose_mode.py               # Full body pose detection logic
└── requirements.txt           # Python dependencies
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/subway-surfers-gesture-control.git
   cd subway-surfers-gesture-control
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

### Option A — GUI (Recommended)
```bash
python gui_control.py
```
A window will open with two buttons to choose your mode.

### Option B — CLI
```bash
python main.py
```
Then type `1` or `2` to choose your mode.

---

## 🕹️ Controls

### ✋ Finger Gesture Mode

| Fingers Up | Action       |
|------------|--------------|
| 1 finger   | ⬅️ Move Left  |
| 2 fingers  | ➡️ Move Right |
| 3 fingers  | ⬆️ Jump       |
| 4 fingers  | ⬇️ Roll       |

### 🧍 Full Body Pose Mode

| Body Movement         | Action              |
|-----------------------|---------------------|
| Lean Left             | ⬅️ Move Left         |
| Lean Right            | ➡️ Move Right        |
| Jump up               | ⬆️ Jump              |
| Crouch down           | ⬇️ Roll              |
| Join both hands (hold)| ▶️ Start / Revive    |

---

## 📦 Requirements

- Python 3.8+
- Webcam
- `opencv-python`
- `mediapipe`
- `pyautogui`

---

## 📌 Notes

- Press **`q`** in the camera window to quit at any time.
- For pose mode, make sure your **full upper body** is visible in the frame.
- Works best in a well-lit room.

---

## 🙌 Credits

Built with [MediaPipe](https://mediapipe.dev/) and [OpenCV](https://opencv.org/).
