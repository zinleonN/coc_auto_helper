import asyncio
import pyautogui as pa
import logging
import random


from src.tools import sleep
from src.pyautogui_common import (
    clickImage,
    locateImages,
    detect_best_direction,
)

attack_army_names = [
    "attack_army_special_goblin", "attack_army_goblin", "attack_army_dragon"
    ]

    # heros 
attack_hero_names = [
        "attack_hero_archer_queen", "attack_hero_minion_prince" 
]

async def choose_suitable_attack_target():
   while True:
        while locateImages("attack_next_target") == None:
            sleep(1)
        for i in range(10):
            pa.scroll(-500)
        move_func, min_projected_points = await detect_best_direction()

        if move_func == None:
            logging.info("No suitable attack target found.")
            clickImage("attack_next_target")
            continue
        logging.info(f"best move function: {move_func.__name__}")
        return move_func, min_projected_points

def place_armys(move_func, projected_points):
    move_func()
    i = 0
    for name in attack_army_names:
        location = locateImages(name,color_sensitive=True)
        if location is None:
            continue
        pa.click(location,duration=0.2)
        while locateImages(name, color_sensitive=True):
            t = random.choice(projected_points)
            pa.moveTo(*t,duration=0.2)
            pa.click()
            sleep(0.2)
            pa.click()

    t = random.choice(projected_points)
    for hero_name in attack_hero_names:
        clickImage(hero_name)
        pa.click(*t,duration=0.2)


        


def attack():
    logging.info("Starting attack sequence...")

    if clickImage("attack_1", "attack_2") != 0:
        return -1
    if clickImage("search_1") != 0:
        return -1

    move_func, projected_points = asyncio.run(choose_suitable_attack_target())
    place_armys(move_func,projected_points)


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
