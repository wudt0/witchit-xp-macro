import pyautogui
import time
import numpy as np

w, h = pyautogui.size()  # Get the width and height of the screen
currentMouseX, currentMouseY = pyautogui.position()  # Get the current mouse position

while True:
    x = np.random.randint(940, 980)
    y = np.random.randint(530, 550)
    pyautogui.moveTo(x, y, duration=2.7)  # Move the mouse to a random position
    time.sleep(3)  # Wait for 1 second before the next move