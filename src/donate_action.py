import pyautogui as pa
import logging


from src.tools import sleep
from src.pyautogui_common import (
    clickImage,
    locateImages,
    detect_best_direction,
)

def ramdon_donate():
    pass
    army_name = [
        "donate_army_giant", "donate_army_miner","donate_army_archer", "donate_army_barbarian",  "donate_army_goblin", 
        "donate_army_wall_breaker", "donate_army_balloon", "donate_army_wizard", "donate_army_healer", 
        "donate_army_dragon", "donate_army_pekka", "donate_army_baby_dragon", "donate_army_miner",
        "donate_army_electro_dragon", "donate_army_yeti", "donate_army_dragon_rider", "donate_army_electro_titan", 
        "donate_army_root_rider", "donate_army_minion", "donate_army_thrower", "donate_army_mi", "donate_army_electro_wizard",
        "donate_lighting", "donate_posion"
        ]
    
    while clickImage(*army_name, color_sensitive=True) == 0:
        pass

def donate():
    logging.info("Starting donation sequence...")
    need_resource = False

    clickImage("donate_start")

    while True:
        if clickImage("donate_1") == 0:
            ramdon_donate()
            need_resource = True
        elif clickImage("donate_locate") == 0:
            pass
        else:
            clickImage("donate_back")
            return need_resource
        
