import mediapipe as mp
import util
import pyautogui

mpHands = mp.solutions.hands
scr_w, scr_h = pyautogui.size()


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]


def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * scr_w)
        y = int(index_finger_tip.y * scr_h)
        pyautogui.moveTo(x, y)


def is_right_click(landmarks_list, thumb_ring_dist):
    return (
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
        thumb_ring_dist > 100
    )


def is_left_click(landmarks_list, thumb_ring_dist):
    return (
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
        thumb_ring_dist > 100
    )

def detect_gesture(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:

        index_finger_tip = find_finger_tip(processed)
        thumb_ring_dist = util.get_distance([landmarks_list[4], landmarks_list[16]])

        # FUNC 1 --> Move cursor
        if thumb_ring_dist < 50 and util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
            move_mouse(index_finger_tip)
        
        # FUNC 2 --> Right click
        if is_right_click(landmarks_list, thumb_ring_dist):
            pyautogui.click(button='right')

        # FUNC 3 --> Left click
        if is_left_click(landmarks_list, thumb_ring_dist):
            pyautogui.click(button='left')
