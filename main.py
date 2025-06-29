import src.actions as act
import logging

def main():
    i = 1
    while i < 9:
        logging.info(f"Attack iteration {i + 1}")
        act.attack()
        i += 1
        act.donate()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # main()
    act.detect()