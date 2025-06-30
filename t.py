import pyautogui


location = pyautogui.locateOnScreen('image.png', confidence=0.8)
pyautogui.moveTo(location)