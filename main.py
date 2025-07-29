import pydirectinput
import time
import numpy as np
import pyautogui
from pyautogui import ImageNotFoundException

def random_movement():
    """Simulates random movement by pressing W, A, S, or D for a random duration."""
    key = np.random.choice(['w', 'a', 's', 'd'])
    duration = np.random.uniform(0.1, 0.5)
    pydirectinput.keyDown(key)
    time.sleep(duration)
    pydirectinput.keyUp(key)


def random_rotation():
    """Simulates random rotation by moving the mouse horizontally."""
    x_offset = np.random.randint(-200, 200)
    pydirectinput.moveRel(x_offset, 0, duration=0.8, relative=True)


def random_jump():
    """Simulates a jump by pressing the spacebar."""
    pydirectinput.press('space')


def click_ready_button():
    """Detects and clicks the 'Ready' button if it appears on the screen with enough confidence."""
    try:
        location = pyautogui.locateCenterOnScreen('ready.png', confidence=0.9)
        if location:
            pyautogui.click(location)
    except ImageNotFoundException:
        print("Ready button not found (confidence too low or not present).")


while True:
    click_ready_button()
    action = np.random.choice(
        ['move', 'rotate', 'jump'],
        p=[0.48, 0.48, 0.04]  # 48% move, 48% rotate, 4% jump
    )
    if action == 'move':
        random_movement()
    elif action == 'rotate':
        random_rotation()
    elif action == 'jump':
        random_jump()
    time.sleep(np.random.uniform(0.1, 0.5))