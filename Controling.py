from concurrent.futures import thread
from math import fabs
from mimetypes import init
import mouse as m
import time
import random

import msvcrt as keyboard


class Controling:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_direction = ""
        self.stop = False

    def main(self):

        while True:
            if keyboard.getch().decode("utf-8") == "r":
                print("Right")
                self.move_mouse("Right", 0.5)
            elif keyboard.getch().decode("utf-8") == "l":
                print("Left")
                self.move_mouse("Left", 0.5)
            elif keyboard.getch().decode("utf-8") == "u":
                print("Up")
                self.move_mouse("Up", 0.5)
            elif keyboard.getch().decode("utf-8") == "d":
                print("Down")
                self.move_mouse("Down", 0.5)
            elif keyboard.getch().decode("utf-8") == "b":
                print("Blink")
                self.move_mouse("Blink", 0.5)
            elif keyboard.getch().decode("utf-8") == "q":
                print("Quit")
                break

    def move_mouse(self, direction):

        if (direction == "r" and self.prev_direction == "l") or (
            direction == "l" and self.prev_direction == "r"
        ):
            self.stop = True
            self.prev_direction = None
        elif direction == "rl":
            self.stop = False
            self.move_loop("r", 0)
            self.prev_direction = "r"

        elif direction == "lr":
            self.stop = False
            self.move_loop("l", 0)
            self.prev_direction = "l"

        elif direction == "rl":
            self.stop = False
            self.move_loop("r", 0)
            self.prev_direction = "r"

        elif direction == "l":
            self.stop = False
            thread.start_new_thread(self.move_loop, ("l", 1))
            self.prev_direction = "l"

        elif direction == "r":
            self.stop = False
            thread.start_new_thread(self.move_loop, ("r", 1))
            self.prev_direction = "r"

    def move_loop(self, direction, time):
        if time == 0:
            if direction == "r":
                self.x += 10
                m.move(self.x, self.y)
            elif direction == "l":
                self.x -= 10
                m.move(self.x, self.y)

        else:
            while True:
                if direction == "r":
                    self.x += 1
                    m.move(self.x, self.y)
                elif direction == "l":
                    self.x -= 1
                    m.move(self.x, self.y)

                if self.stop:
                    break


if __name__ == "__main__":
    cn = Controling(960, 540)
    cn.main()
