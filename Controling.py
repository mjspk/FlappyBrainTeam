import threading
import time as t
import pyautogui as pyautogui
import msvcrt as keyboard


class Controling:
    def __init__(self):
        size = pyautogui.size()
        self.width = size[0]
        self.height = size[1]
        self.x = self.width / 2
        self.y = self.height / 2
        self.prev_direction = None
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
        elif (direction == "u" and self.prev_direction == "d") or (
            direction == "d" and self.prev_direction == "u"
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

        elif direction == "ud":
            self.stop = False
            self.move_loop("u", 0)
            self.prev_direction = "u"

        elif direction == "du":
            self.stop = False
            self.move_loop("d", 0)
            self.prev_direction = "d"

        elif direction == "l":
            self.stop = False
            threading.Thread(target=self.move_loop, args=("l", 1)).start()
            self.prev_direction = "l"

        elif direction == "r":
            self.stop = False
            threading.Thread(target=self.move_loop, args=("r", 1)).start()
            self.prev_direction = "r"

        elif direction == "u":
            self.stop = False
            threading.Thread(target=self.move_loop, args=("u", 1)).start()
            self.prev_direction = "u"
        elif direction == "d":
            self.stop = False
            threading.Thread(target=self.move_loop, args=("d", 1)).start()
            self.prev_direction = "d"
        elif direction == "b":
            self.stop = False
            pyautogui.click()
            self.prev_direction = None
        elif direction == "bb":
            self.stop = False
            pyautogui.doubleClick()
            self.prev_direction = None
        elif direction == "rb":
            self.stop = False
            pyautogui.rightClick()
            self.prev_direction = None

    def move_loop(self, direction, time):
        if time == 0:
            if direction == "r":
                if self.x < self.width:
                    self.x += 10
                    pyautogui.moveTo(self.x, self.y)
            elif direction == "l":
                if self.x > 0:
                    self.x -= 10
                    pyautogui.moveTo(self.x, self.y)
            elif direction == "u":
                if self.y > 0:
                    self.y -= 10
                    pyautogui.moveTo(self.x, self.y)
            elif direction == "d":
                if self.y < self.height:
                    self.y += 10
                    pyautogui.moveTo(self.x, self.y)

        else:
            while True:
                if direction == "r":
                    if self.x < self.width:
                        self.x += 10
                        pyautogui.moveTo(self.x, self.y)
                elif direction == "l":
                    if self.x > 0:
                        self.x -= 10
                        pyautogui.moveTo(self.x, self.y)
                elif direction == "u":
                    if self.y > 0:
                        self.y -= 10
                        pyautogui.moveTo(self.x, self.y)
                elif direction == "d":
                    if self.y < self.height:
                        self.y += 10
                        pyautogui.moveTo(self.x, self.y)
                t.sleep(0.1)
                if self.stop:
                    break


if __name__ == "__main__":
    cn = Controling(960, 540)
    cn.main()
