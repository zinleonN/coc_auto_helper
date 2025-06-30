import pyautogui as pa
import logging


from src.tools import sleep
from src.pyautogui_common import (
    clickImage,
    locateImages,
    detect_best_direction,
    place_army
)

attack_army_names = [
    "attack_army_special_goblin", "attack_army_goblin",
    ]

    # heros 
attack_hero_names = [
        "attack_hero_archer_queen", "attack_hero_minion_prince" 
]

def choose_suitable_attack_target():
   while True:
        while locateImages("attack_next_target") == None:
            sleep(1)
        for i in range(10):
            pa.scroll(-500)
        best_direction = detect_best_direction()
        if best_direction == None:
            logging.info("No suitable attack target found.")
            clickImage("attack_next_target")
            continue
        return best_direction

def place_armys(direction):
    need_locate = True
    while True:
        location = locateImages(*attack_army_names, color_sensitive=True)
        if location is None:
            logging.info("No attack army found")
            break
        place_army(location, direction, need_locate)
        if need_locate:
            need_locate = False
    
    for hero in attack_hero_names:
        location = locateImages(hero, color_sensitive=True)
        if location is None:
            continue
        place_army(location, direction, need_locate)
        


def attack():
    logging.info("Starting attack sequence...")

    if clickImage("attack_1", "attack_2") != 0:
        return -1
    if clickImage("search_1") != 0:
        return -1

    best_direction = choose_suitable_attack_target()
    place_armys(best_direction)


    logging.info("Waiting for attack to complete...")
    while True:
        sleep(6)
        location = locateImages("attack_back")
        if location == None:
            continue
        sleep(3)
        clickImage("attack_back")
        sleep(8)
        # TODO  Daily Rewards confirmation
        res = locateImages("attack_comfirm_resource")
        if res is not None:
            pa.click(res)
        return
