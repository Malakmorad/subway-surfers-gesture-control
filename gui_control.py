import tkinter as tk
from tkinter import font
import threading
from pose_mode import run_pose_mode
from finger_gesture_control import run_finger_mode


def launch_finger():
    btn_finger.config(state="disabled")
    btn_pose.config(state="disabled")
    status_label.config(text="🟢 Finger Gesture Mode Running...\nPress 'q' in the camera window to stop.")
    t = threading.Thread(target=run_finger_mode, daemon=True)
    t.start()


def launch_pose():
    btn_finger.config(state="disabled")
    btn_pose.config(state="disabled")
    status_label.config(text="🟢 Pose Detection Mode Running...\nPress 'q' in the camera window to stop.")
    t = threading.Thread(target=run_pose_mode, daemon=True)
    t.start()


# Window setup
root = tk.Tk()
root.title("Subway Surfers Gesture Controller")
root.geometry("420x300")
root.resizable(False, False)
root.configure(bg="#1a1a2e")

title_font = font.Font(family="Helvetica", size=16, weight="bold")
btn_font = font.Font(family="Helvetica", size=13)
small_font = font.Font(family="Helvetica", size=10)

tk.Label(root, text="🎮 Subway Surfers", font=title_font,
         bg="#1a1a2e", fg="#e94560").pack(pady=(20, 4))
tk.Label(root, text="Gesture Controller", font=btn_font,
         bg="#1a1a2e", fg="#ffffff").pack(pady=(0, 20))

btn_finger = tk.Button(root, text="✋  Finger Gesture Control", font=btn_font,
                       bg="#e94560", fg="white", activebackground="#c73652",
                       relief="flat", padx=10, pady=8, width=24,
                       command=launch_finger)
btn_finger.pack(pady=6)

btn_pose = tk.Button(root, text="🧍  Full Body Pose Control", font=btn_font,
                     bg="#0f3460", fg="white", activebackground="#0a2540",
                     relief="flat", padx=10, pady=8, width=24,
                     command=launch_pose)
btn_pose.pack(pady=6)

status_label = tk.Label(root, text="Select a control mode above to start.",
                        font=small_font, bg="#1a1a2e", fg="#aaaaaa",
                        wraplength=380, justify="center")
status_label.pack(pady=(16, 0))

root.mainloop()
