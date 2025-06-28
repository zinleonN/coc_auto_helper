import src.actions as act
import logging

def main():
    i = 0
    while i < 5:
        logging.info(f"Attack iteration {i + 1}")
        act.attack()
        i += 1

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()