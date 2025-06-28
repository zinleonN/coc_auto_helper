import pyautogui as pa
import logging

from src.tools import sleep
import src.pyautogui_common as common

def clickImage(*image_names, color_sensitive=False):
    logging.info(f"Attempting to click on images: {image_names}")
    location = common.locateImages(*image_names, color_sensitive=color_sensitive)
    if location:
        pa.click(location)
        return 0
    else:
        logging.error(f"Failed to find images: {image_names}")
        exit(-1)

def attack():
    logging.info("Starting attack sequence...")

    clickImage("attack_1")
    clickImage("search_1")

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
        return
