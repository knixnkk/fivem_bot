# Overview
This Python script automates interactions in the game Meow Town Roleplay by detecting a specific in-game image (hook icon) and pressing the space key when certain conditions are met. It uses computer vision techniques to match the template image with the screen content and checks pixel colors around the detected object. When a match is found, the script simulates a key press to perform actions in the game.

## Requirements
- **Python Libraries**:
- *opencv-python (cv2)*: For image processing and template matching.
- *numpy*: For efficient array operations and pixel analysis.
- *mss*: For screen capture of the game window.
- *pywinauto*: To interact with the game window (detect its position and size).
- *pydirectinput*: To simulate key presses.

## Install these dependencies using the following command:

```bash
pip install opencv-python numpy mss pywinauto pydirectinput
```
## Other Requirements:
- *Template Image*: Ensure that hook.png (the image you want to detect) is in the same directory as the script.

## How it Works
- *Window Detection*: The script connects to the game window using the pywinauto library to get the window's rectangle and size.
- *Screen Capture*: The mss library captures a specific portion of the screen, defined by coordinates based on the detected window size and position.
- *Template Matching*: The script uses OpenCV's matchTemplate method to detect the hook icon (hook.png) within the captured region of the screen. When a match with a confidence score of 0.8 or higher is found, the coordinates are logged, and a circle is drawn at the center of the matched location.
- *Color Check*: The script examines the pixel colors around the detected object. If certain pixels match a predefined color threshold (similar to RGB [147, 146, 144] with a tolerance of 30), the space key is pressed using pydirectinput.
- *FPS Display*: The script calculates and prints the frame rate (frames per second) to help monitor the script's performance.
- *Real-Time Display*: A window shows the screen capture with real-time tracking, and the script will continue until you press q to quit.

## How to Use
- *Setup*: Ensure the game Meow Town Roleplay is running.
- *Run the Script*: Execute the Python script:

```bash
python main.py
```

The script will automatically detect the game window and begin capturing the screen.
If the hook icon is detected and certain color conditions are met, the script will simulate a key press (space).

- *Quit the Script*: To stop the script, press the q key in the OpenCV window.

## Customization
- *Adjust Capture Region*: The screen capture region is defined by top_left_x, top_left_y, bottom_right_x, and bottom_right_y. You can modify these values to fit your screen layout.
- *Change Template*: Replace hook.png with your desired template image if needed. Ensure the template image is in the same directory and adjust the code if needed for a different template size.
- *Modify Thresholds*: You can adjust the template matching threshold (match_threshold) and the color comparison threshold (color_threshold) to fine-tune detection accuracy.

## Known Limitations
The script assumes the game window title contains "MEOW TOWN ROLEPLAY". If the window title is different, you will need to adjust the regex in Application().connect and window() functions.
The game must be visible and not minimized for the script to work properly.
