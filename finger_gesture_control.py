import cv2
import mediapipe as mp
import pyautogui
import time

# Setup Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Fingertip landmark IDs
tip_ids = [4, 8, 12, 16, 20]


def run_finger_mode():
    cap = cv2.VideoCapture(0)
    prev_action_time = time.time()
    delay = 0.5  # seconds between each command

    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        fingers = []

        if result.multi_hand_landmarks:
            for hand_landmark in result.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmark.landmark):
                    lm_list.append((int(lm.x * w), int(lm.y * h)))

                # Thumb (left or right)
                if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers
                for i in range(1, 5):
                    if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = fingers.count(1)
                cv2.putText(frame, f"Fingers: {total_fingers}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

                # Execute action based on finger count
                current_time = time.time()
                if current_time - prev_action_time > delay:
                    if total_fingers == 1:
                        pyautogui.press("left")
                        print("⬅️ Move Left")
                    elif total_fingers == 2:
                        pyautogui.press("right")
                        print("➡️ Move Right")
                    elif total_fingers == 3:
                        pyautogui.press("up")
                        print("⬆️ Jump")
                    elif total_fingers == 4:
                        pyautogui.press("down")
                        print("⬇️ Roll")
                    prev_action_time = current_time

                mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Finger Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
