import os
import time

from .gol import Universe


def main():
    universe = Universe.randomized(20, 20)
    print universe

    while universe.next():
        time.sleep(0.1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print universe

if __name__ == "__main__":
    main()
