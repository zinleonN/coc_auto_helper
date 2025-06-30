import random
import time
import os
from pathlib import Path



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


