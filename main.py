import cv2
import mediapipe as mp
import util
import functionality

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode= False,
    model_complexity= 1,
    min_detection_confidence= 0.7, 
    min_tracking_confidence= 0.7,
    max_num_hands= 1)

def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # else:
            #     frame_height, frame_width = frame.shape[:2]
            #     print(f"Frame Width: {frame_width}, Frame Height: {frame_height}")
            
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmarks_list = []

            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                
                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))

                #print(landmarks_list)
            
            # IDENTIFIES GESTURES
            functionality.detect_gesture(frame, landmarks_list, processed)

            cv2.imshow("FRAME", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()