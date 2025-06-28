import pyautogui as pa
import logging

from src.tools import sleep
import src.pyautogui_common as common

def clickImage(*image_names, color_sensitive=False):
    # 限制输出图片名数量，避免日志过长
    max_names = 5
    names_display = image_names[:max_names]
    names_str = ', '.join(str(n) for n in names_display)
    if len(image_names) > max_names:
        names_str += ', ...'
    logging.info(f"Attempting to click on images: [{names_str}]")
    location = common.locateImages(*image_names, color_sensitive=color_sensitive)
    if location:
        pa.click(location)
        return 0
    else:
        logging.error(f"Failed to find images: [{names_str}]")
        return -1

def ramdon_donate():
    pass
    army_name = [
        "donate_army_miner","donate_army_archer", "donate_army_barbarian", "donate_army_giant", "donate_army_goblin", 
        "donate_army_wall_breaker", "donate_army_balloon", "donate_army_wizard", "donate_army_healer", 
        "donate_army_dragon", "donate_army_pekka", "donate_army_baby_dragon", "donate_army_miner",
        "donate_army_electro_dragon", "donate_army_yeti", "donate_army_dragon_rider", "donate_army_electro_titan", 
        "donate_army_root_rider", "donate_army_minion", "donate_army_thrower", "donate_army_mi", "donate_army_electro_wizard"]
    
    while clickImage(*army_name, color_sensitive=True) == 0:
        pass

def attack():
    logging.info("Starting attack sequence...")

    if clickImage("attack_1", "attack_2") != 0:
        return -1
    if clickImage("search_1") != 0:
        return -1

    sleep(5)
    common.moveToRightUp()

    while clickImage("attack_army_special_goblin", color_sensitive=True) == 0:
        common.moveFromTo((0.38, 0.13), (0.74, 0.60))


    clickImage("attack_queen")
    common.moveFromTo((0.24, 0.20), (0.24, 0.20))

    logging.info("Waiting for attack to complete...")
    while True:
        sleep(6)
        location = common.locateImages("attack_back")
        if location == None:
            continue
        sleep(3)
        clickImage("attack_back")
        sleep(8)
        # TODO  Daily Rewards confirmation
        return

def donate():
    logging.info("Starting donation sequence...")

    clickImage("donate_start")

    while True:
        if clickImage("donate_1") == 0:
            ramdon_donate()
        elif clickImage("donate_locate") == 0:
            pass
        else:
            clickImage("donate_back")
            return 0
        

