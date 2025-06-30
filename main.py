import src.pyautogui_common as pa
import pyautogui
import logging

from src.attack_action import attack

from src.tools import sleep

def back_to_game():
    pyautogui.hotkey('alt', 'tab')
    sleep(1.5)
    for i in range(20):
        pyautogui.scroll(-500)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # main()
    back_to_game()
    # pa.detect_best_direction()
    attack()

