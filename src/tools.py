import random
import time
import os
from pathlib import Path



src_dir = Path(__file__).parent
images_dir = src_dir / 'images'

def fluctuate_number(n):
    if n == 0:
        return 0.0
    n_abs = abs(n)
    # 取数量级（个位、十位、百位...）
    magnitude = 10 ** (len(str(int(n_abs))) - 1)
    low = n - magnitude
    high = n + magnitude
    result = random.uniform(low, high)
    return max(round(result, 2), 1)


def sleep(n):
    time.sleep(fluctuate_number(n))


def image_path(name):
    name = name if name.endswith('.png') else f"{name}.png"
    path = images_dir / name
    return str(path.resolve()) if path.exists() else None

