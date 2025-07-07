import random
import time
import os
from pathlib import Path
import math


src_dir = Path(__file__).parent
images_dir = src_dir / 'images'

def fluctuate_number(n):
    if n == 0:
        return 0.0
    magnitude = max(0.1, abs(n) / 10 * 2)
    low = n - magnitude
    high = n + magnitude
    result = random.uniform(low, high)
    return max(0.5, result)


def sleep(n):
    time.sleep(fluctuate_number(n))


def image_path(name):
    name = name if name.endswith('.png') else f"{name}.png"
    path = images_dir / name
    return str(path.resolve()) if path.exists() else None

def random_offset(n):
    offset = n / 10
    return round(random.uniform(n - offset, n + offset), 3)

def distance(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


