import cv2
import pyautogui
from time import time
from math import hypot
import mediapipe as mp


def run_pose_mode():
    mp_pose = mp.solutions.pose
    pose_video = mp_pose.Pose(static_image_mode=False, model_complexity=1,
                              min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    def detectPose(image, pose, draw=False):
        output_image = image.copy()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(imageRGB)
        if results.pose_landmarks and draw:
            mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                      connections=mp_pose.POSE_CONNECTIONS)
        return output_image, results

    def checkHandsJoined(image, results, draw=False):
        output_image = image.copy()
        height, width, _ = image.shape
        left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        distance = hypot(left.x - right.x, left.y - right.y)
        if draw:
            cv2.putText(output_image, f'Distance: {round(distance, 5)}', (10, 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        joined = "Hands Joined" if distance < 0.1 else "Hands Not Joined"
        return output_image, joined

    def checkLeftRight(image, results, draw=False):
        output_image = image.copy()
        height, width, _ = image.shape
        right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_x = int(right.x * width)

        if right_x < width * 0.4:
            pos = "Left"
        elif right_x > width * 0.6:
            pos = "Right"
        else:
            pos = "Center"

        print(f"Right Shoulder X: {right_x} / Frame Width: {width} → Relative: {right.x:.2f} → Position: {pos}")

        if draw:
            cv2.putText(output_image, pos, (10, 60),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

        return output_image, pos

    def checkJumpCrouch(image, results, MID_Y=250, draw=False):
        output_image = image.copy()
        height, width, _ = image.shape
        left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        actual_mid_y = int((left.y + right.y) * height // 2)

        upper = MID_Y - 20
        lower = MID_Y + 20

        if actual_mid_y < upper:
            posture = "Jumping"
        elif actual_mid_y > lower:
            posture = "Crouching"
        else:
            posture = "Standing"

        print(f"actual_mid_y: {actual_mid_y}, MID_Y: {MID_Y}, posture: {posture}")

        if draw:
            cv2.putText(output_image, posture, (5, height - 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

        return output_image, posture

    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, 1280)
    camera_video.set(4, 960)
    cv2.namedWindow('Subway Surfers with Pose Detection', cv2.WINDOW_NORMAL)

    time1 = 0
    game_started = False
    x_pos_index = 1
    y_pos_index = 1
    MID_Y = None
    counter = 0
    num_of_frames = 10

    while camera_video.isOpened():
        ok, frame = camera_video.read()
        if not ok:
            continue
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape

        frame, results = detectPose(frame, pose_video, draw=game_started)

        if results.pose_landmarks:
            if game_started:
                frame, horizontal_position = checkLeftRight(frame, results, draw=True)
                print("Detected Direction:", horizontal_position)

                if (horizontal_position == 'Left' and x_pos_index != 0) or \
                        (horizontal_position == 'Center' and x_pos_index == 2):
                    pyautogui.press('left')
                    x_pos_index -= 1
                elif (horizontal_position == 'Right' and x_pos_index != 2) or \
                        (horizontal_position == 'Center' and x_pos_index == 0):
                    pyautogui.press('right')
                    x_pos_index += 1
            else:
                cv2.putText(frame, 'JOIN BOTH HANDS TO START THE GAME.', (5, frame_height - 10),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

            if checkHandsJoined(frame, results)[1] == 'Hands Joined':
                counter += 1
                if counter == num_of_frames:
                    if not game_started:
                        game_started = True
                        left_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * frame_height)
                        right_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * frame_height)
                        MID_Y = abs(right_y + left_y) // 2
                        pyautogui.click(x=1300, y=800, button='left')
                    else:
                        pyautogui.press('space')
                    counter = 0
            else:
                counter = 0

            if MID_Y:
                frame, posture = checkJumpCrouch(frame, results, MID_Y, draw=True)
                if posture == 'Jumping' and y_pos_index == 1:
                    pyautogui.press('up')
                    y_pos_index += 1
                elif posture == 'Crouching' and y_pos_index == 1:
                    pyautogui.press('down')
                    y_pos_index -= 1
                elif posture == 'Standing' and y_pos_index != 1:
                    y_pos_index = 1
        else:
            counter = 0

        time2 = time()
        if (time2 - time1) > 0:
            fps = 1.0 / (time2 - time1)
            cv2.putText(frame, 'FPS: {}'.format(int(fps)), (10, 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
        time1 = time2

        cv2.imshow('Subway Surfers with Pose Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera_video.release()
    cv2.destroyAllWindows()
