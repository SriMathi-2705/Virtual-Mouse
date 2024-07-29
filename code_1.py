import cv2
import mediapipe as mp
import pyautogui

# Initialize video capture, MediaPipe hand detector, and get screen dimensions
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            # Draw landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Variables to store index finger and thumb coordinates
            index_x, index_y = 0, 0
            thumb_x, thumb_y = 0, 0

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Get coordinates of the index finger (landmark id 8)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                # Get coordinates of the thumb (landmark id 4)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

            # Perform mouse actions based on the distance between index finger and thumb
            if abs(index_y - thumb_y) < 20:
                pyautogui.click()
                pyautogui.sleep(1)
            elif abs(index_y - thumb_y) < 100:
                pyautogui.moveTo(index_x, index_y)

    # Display the frame
    cv2.imshow('Virtual Mouse', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
