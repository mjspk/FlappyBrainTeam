from mimetypes import init
import mouse as m
import time
import random

import msvcrt as keyboard


class Controling:
    def main(self):
        x = 960
        y = 540
        while True:
            if keyboard.getch().decode("utf-8") == "r":
                print("Right")
                # move mouse 1o to right
                x = x + 10
                m.move(x, y)
            elif keyboard.getch().decode("utf-8") == "l":
                print("Left")
                # move mouse 1o to left
                x = x - 10
                m.move(x, y)
            elif keyboard.getch().decode("utf-8") == "u":
                print("Up")
                # move mouse 1o up
                y = y - 10
                m.move(x, y)
            elif keyboard.getch().decode("utf-8") == "d":
                print("Down")
                # move mouse 1o down
                y = y + 10
                m.move(x, y)
            elif keyboard.getch().decode("utf-8") == "c":
                print("Click")
                m.click()
            elif keyboard.getch().decode("utf-8") == "b":
                print("Double click")
                m.right_click()

            elif keyboard.getch().decode("utf-8") == "q":
                print("Quit")
                break


if __name__ == "__main__":

    cn = Controling()
    cn.main()
