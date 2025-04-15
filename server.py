from flask import Flask
import time
import pyautogui
import cv2
import numpy as np

app = Flask(__name__)

# Load reference images
meteor_img = cv2.imread('meteor.png', 0)  # Replace with actual meteorite image
bomb_img = cv2.imread('bomb.png', 0)  # Replace with actual bomb image

def detect_and_click():
    time.sleep(1)  # Wait for game to start

    while True:
        # Capture screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Match template for meteor
        res_meteor = cv2.matchTemplate(frame_gray, meteor_img, cv2.TM_CCOEFF_NORMED)
        loc_meteor = np.where(res_meteor >= 0.7)

        # Match template for bomb
        res_bomb = cv2.matchTemplate(frame_gray, bomb_img, cv2.TM_CCOEFF_NORMED)
        loc_bomb = np.where(res_bomb >= 0.7)

        # Convert bomb locations to set
        bomb_positions = set(zip(*loc_bomb[::-1]))

        for pt in zip(*loc_meteor[::-1]):  # Iterate over meteorite locations
            if pt not in bomb_positions:  # Avoid bombs
                pyautogui.click(pt[0], pt[1])
        
        time.sleep(0.5)  # Adjust speed

@app.route('/start-bot')
def start_bot():
    detect_and_click()
    return "Bot Started"

if __name__ == '__main__':
    app.run(port=5000)
