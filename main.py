import pydirectinput
import time
import numpy as np
import pyautogui
from pyautogui import ImageNotFoundException as PyAutoGUIImageNotFoundException
import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageGrab
import re


def count_players():
    """Extracts the player count from the screen using OCR on the scoreboard."""
    try:
        pydirectinput.keyDown('tab')
        time.sleep(1.0) 

        screenshot = ImageGrab.grab()
        crop_box = (760, 0, 1160, 50)
        cropped = screenshot.crop(crop_box)

        gray = ImageOps.grayscale(cropped)
        resized = gray.resize((gray.width * 2, gray.height * 2), Image.LANCZOS)
        enhanced = ImageEnhance.Contrast(resized).enhance(2.5)

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(resized, config=custom_config)


        print(f"OCR raw text: {text}")

        match = re.search(r'(\d{1,2})\s*/\s*\d{1,2}', text)
        if match:
            player_count = int(match.group(1))
            return player_count
        else:
            print(f"OCR failed, text read: {text}")
            return 0

    except Exception as e:
        print(f"Error during OCR player count: {e}")
        return 0

    finally:
        pydirectinput.keyUp('tab')

def random_movement():
    """Simulates random movement by pressing W, A, S, or D for a random duration."""
    key = np.random.choice(['a', 's', 'd'])
    duration = np.random.uniform(0.5, 1.2)
    pydirectinput.keyDown(key)
    time.sleep(duration)
    pydirectinput.keyUp(key)


def random_rotation():
    """Simulates smoother horizontal mouse rotation."""
    total_offset = np.random.randint(-1200, 1200)
    steps = 5
    delay_per_step = 0.01

    step_size = total_offset / steps

    for _ in range(steps):
        pydirectinput.moveRel(int(step_size), 0, relative=True)
        time.sleep(delay_per_step)


def random_jump():
    """Simulates a jump by pressing the spacebar."""
    pydirectinput.press('space')


def random_left_click():
    """Simulates a simple left mouse click."""
    pydirectinput.click(button='left')
    time.sleep(np.random.uniform(0.2, 1))


def random_q_right_click():
    """Simulates pressing 'q' and then right-clicking."""
    pydirectinput.press('q')
    pydirectinput.click(button='right')


def click_ready_button():
    """Detects and clicks the 'Ready' button if it appears on the screen with enough confidence."""
    try:
        location = pyautogui.locateCenterOnScreen('ready.png', confidence=0.9)
        if location:
            pyautogui.click(location)
    except (PyAutoGUIImageNotFoundException):
        print("Ready button not found (confidence too low or not present).")


def exit_and_find_new_game():
    """Exits the current game and finds a new one."""
    print("Player count below 3, reconnecting...")
    pydirectinput.press('esc')
    time.sleep(1)
    for button_name in ['exit.png', 'play.png', 'quickmatch.png', 'findgame.png']:
        location = pyautogui.locateCenterOnScreen(button_name, confidence=0.9)
        if location:
            pyautogui.click(location)
            time.sleep(1)
        else:
            print(f"Could not find {button_name}, aborting reconnect.")
            break


last_q_right_click_time = time.time()
while True:
    pydirectinput.keyDown('w')
    if click_ready_button():
        click_ready_button()
        time.sleep(15)
    player_count = count_players()
    if player_count < 3 and player_count != 0:
        exit_and_find_new_game()
        time.sleep(5)
    random_left_click()
    action = np.random.choice(
        ['move', 'rotate', 'jump'],
        p=[0.45, 0.45, 0.10]  # 45% move, 45% rotate, 10% jump
    )
    if action == 'move':
        random_movement()
    elif action == 'rotate':
        random_rotation()
    elif action == 'jump':
        random_jump()

    if time.time() - last_q_right_click_time > np.random.uniform(15, 23):
        random_q_right_click()
        last_q_right_click_time = time.time()

    time.sleep(np.random.uniform(0.1, 0.5))