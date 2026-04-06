from pose_mode import run_pose_mode
from finger_gesture_control import run_finger_mode


def main():
    print("=" * 40)
    print("  Subway Surfers Gesture Controller")
    print("=" * 40)
    print("Choose control method:")
    print("  1 - Finger Gesture Control")
    print("  2 - Full Body Pose Control")
    print("=" * 40)

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        print("\n[Finger Gesture Mode] Starting... Press 'q' to quit.")
        run_finger_mode()
    elif choice == "2":
        print("\n[Pose Detection Mode] Starting... Press 'q' to quit.")
        run_pose_mode()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
