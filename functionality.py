import mediapipe as mp
import util
import pyautogui
import numpy as np

mpHands = mp.solutions.hands
scr_w, scr_h = pyautogui.size()

# Initialize previous mouse position
prev_x, prev_y = pyautogui.position()


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]


def move_mouse(index_finger_tip, func):
    global prev_x, prev_y
    
    if index_finger_tip is not None:
        x = index_finger_tip.x * scr_w
        y = index_finger_tip.y * scr_h 

        # Calculate distance moved
        distance = ((x - prev_x) ** 2 + (y - prev_y) ** 2) ** 0.5

        # Adjust sensitivity
        sensitivity = 0.5  # Adjust this value for more or less sensitivity
        new_x = prev_x + (x - prev_x) * sensitivity
        new_y = prev_y + (y - prev_y) * sensitivity

        if func == "move":
            pyautogui.moveTo(new_x, new_y)
        elif func == "drag":
            pyautogui.dragTo(new_x, new_y)

        # Update previous position
        prev_x, prev_y = new_x, new_y


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
        thumb_index_dist = util.get_distance([landmarks_list[4], landmarks_list[8]])

        # FUNC 1 --> Move cursor
        if thumb_ring_dist < 50 and util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
            move_mouse(index_finger_tip, "move")
        
        # FUNC 2 --> Right click
        if is_right_click(landmarks_list, thumb_ring_dist):
            pyautogui.click(button='right')

        # FUNC 3 --> Left click
        if is_left_click(landmarks_list, thumb_ring_dist):
            pyautogui.click(button='left')

        # FUNC 4 --> drag (click and hold)
        if thumb_index_dist <= 30:
            move_mouse(index_finger_tip, "drag")
