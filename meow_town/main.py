import cv2
import numpy as np
import mss
import time 
from pywinauto.application import Application
import pydirectinput

app = Application().connect(title_re=".*MEOW TOWN ROLEPLAY.*")  # Using regex to match
window = app.window(title_re=".*MEOW TOWN ROLEPLAY.*")  # Using regex to match

rect = window.rectangle()

template = cv2.imread('hook.png', cv2.IMREAD_UNCHANGED)
template_height, template_width = template.shape[:2]

top_left_x, top_left_y = 285, 400  
bottom_right_x, bottom_right_y = 520, 600  

threshold_color = np.array([147, 146, 144])
color_threshold = 30 

count = 0

sct = mss.mss()

prev_time = time.time()
fps = 0

while True:
    bbox = {
        'top': rect.top + top_left_y,
        'left': rect.left + top_left_x,
        'width': bottom_right_x - top_left_x,
        'height': bottom_right_y - top_left_y
    }
    
    frame = np.array(sct.grab(bbox)) 
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_frame, gray_template, cv2.TM_CCOEFF_NORMED)

    match_threshold = 0.8  
    loc = np.where(result >= match_threshold)

    for pt in zip(*loc[::-1]): 
        center_x = pt[0] + template_width // 2
        center_y = pt[1] + template_height // 2

        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1) 

        print(f"Center position: ({center_x}, {center_y})")

        positions = [
            (center_x - 19, center_y),  # left
            (center_x + 19, center_y),  # right
            (center_x, center_y - 19),  # top
            (center_x, center_y + 19),  # bottom
        ]

        left_right_similar = False
        top_bottom_similar = False

        left_x, left_y = positions[0]
        right_x, right_y = positions[1]

        if 0 <= left_x < frame.shape[1] and 0 <= left_y < frame.shape[0]:
            left_color = frame[left_y, left_x]  
        else:
            left_color = None

        if 0 <= right_x < frame.shape[1] and 0 <= right_y < frame.shape[0]:
            right_color = frame[right_y, right_x] 
        else:
            right_color = None

        if left_color is not None and right_color is not None:
            left_right_similar = (
                abs(left_color[0] - threshold_color[0]) < color_threshold and
                abs(left_color[1] - threshold_color[1]) < color_threshold and
                abs(left_color[2] - threshold_color[2]) < color_threshold
            ) and (
                abs(right_color[0] - threshold_color[0]) < color_threshold and
                abs(right_color[1] - threshold_color[1]) < color_threshold and
                abs(right_color[2] - threshold_color[2]) < color_threshold
            )

        top_x, top_y = positions[2]
        bottom_x, bottom_y = positions[3]

        if 0 <= top_x < frame.shape[1] and 0 <= top_y < frame.shape[0]:
            top_color = frame[top_y, top_x]  # top
        else:
            top_color = None

        if 0 <= bottom_x < frame.shape[1] and 0 <= bottom_y < frame.shape[0]:
            bottom_color = frame[bottom_y, bottom_x]  # bottom
        else:
            bottom_color = None

        if top_color is not None and bottom_color is not None:
            top_bottom_similar = (
                abs(top_color[0] - threshold_color[0]) < color_threshold and
                abs(top_color[1] - threshold_color[1]) < color_threshold and
                abs(top_color[2] - threshold_color[2]) < color_threshold
            ) and (
                abs(bottom_color[0] - threshold_color[0]) < color_threshold and
                abs(bottom_color[1] - threshold_color[1]) < color_threshold and
                abs(bottom_color[2] - threshold_color[2]) < color_threshold
            )

        if left_right_similar or top_bottom_similar:
            print("Either left-right or top-bottom colors are similar to threshold_color")
            pydirectinput.press('space')
            count += 1
            
    current_time = time.time()
    time_elapsed = current_time - prev_time
    fps = 1 / time_elapsed
    prev_time = current_time

    print(fps)
    
    cv2.imshow('Tracked Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
sct.close()
cv2.destroyAllWindows()
