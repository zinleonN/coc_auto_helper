import src.pyautogui_common as pa
import pyautogui
import logging

from src.attack_action import attack
from src.donate_action import donate

from src.tools import sleep

def back_to_game():
    pyautogui.hotkey('alt', 'tab')
    sleep(1.5)
    for i in range(20):
        pyautogui.scroll(-500)



def main():
    attack_needs = 1
    while True:
        if attack_needs >= 1:
            attack()
            attack_needs -= 1
        else:
            sleep(6)
        
        need = donate()
        if need:
            attack_needs += 1
        else:
            attack_needs += 0.3
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    back_to_game()
    main()  
    

