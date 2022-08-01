import threading
import time as t
import pyautogui as pyautogui
import msvcrt as keyboard


class Controling:
    def __init__(self):
        size = pyautogui.size()
        self.width = size[0]
        self.height = size[1]
        self.prev_direction = None
        self.stop = False

    def move_mouse(self, direction):
        pos = pyautogui.position()
        self.x = pos[0]
        self.y = pos[1]
        if (
            (direction == "r" and self.prev_direction == "l")
            or (direction == "l" and self.prev_direction == "r")
            or (direction == "u" and self.prev_direction == "d")
            or (direction == "d" and self.prev_direction == "u")
            or (direction == "l" and self.prev_direction == "rd")
            or (direction == "r" and self.prev_direction == "ld")
            or (direction == "r" and self.prev_direction == "lu")
            or (direction == "l" and self.prev_direction == "ru")
            or (direction == "u" and self.prev_direction == "rd")
            or (direction == "u" and self.prev_direction == "ld")
            or (direction == "d" and self.prev_direction == "ru")
            or (direction == "d" and self.prev_direction == "lu")
        ):
            self.stop = True
            self.prev_direction = None

        elif (
            direction == "r"
            and self.prev_direction == "u"
            or (direction == "u" and self.prev_direction == "r")
        ):
            self.stop = True
            t.sleep(0.1)
            self.stop = False
            self.prev_direction = "ru"
            threading.Thread(target=self.move_loop, args=("ru", 1)).start()

        elif (
            direction == "r"
            and self.prev_direction == "d"
            or (direction == "d" and self.prev_direction == "r")
        ):
            self.stop = True
            t.sleep(0.1)
            self.stop = False
            self.prev_direction = "rd"
            threading.Thread(target=self.move_loop, args=("rd", 1)).start()

        elif (direction == "l" and self.prev_direction == "u") or (
            direction == "u" and self.prev_direction == "l"
        ):
            self.stop = True
            t.sleep(0.1)
            self.stop = False
            self.prev_direction = "lu"
            threading.Thread(target=self.move_loop, args=("lu", 1)).start()

        elif (direction == "l" and self.prev_direction == "d") or (
            direction == "d" and self.prev_direction == "l"
        ):
            self.stop = True
            t.sleep(0.1)
            self.stop = False
            self.prev_direction = "ld"
            threading.Thread(target=self.move_loop, args=("ld", 1)).start()

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

            elif direction == "ru":
                if self.x < self.width and self.y > 0:
                    self.x += 10
                    self.y -= 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.x < self.width:
                    self.x += 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.y > 0:
                    self.y -= 10
                    pyautogui.moveTo(self.x, self.y)

            elif direction == "rd":
                if self.x < self.width and self.y < self.height:
                    self.x += 10
                    self.y += 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.x < self.width:
                    self.x += 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.y < self.height:
                    self.y += 10
                    pyautogui.moveTo(self.x, self.y)

            elif direction == "lu":
                if self.x > 0 and self.y > 0:
                    self.x -= 10
                    self.y -= 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.x > 0:
                    self.x -= 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.y > 0:
                    self.y -= 10
                    pyautogui.moveTo(self.x, self.y)

            elif direction == "ld":
                if self.x > 0 and self.y < self.height:
                    self.x -= 10
                    self.y += 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.x > 0:
                    self.x -= 10
                    pyautogui.moveTo(self.x, self.y)
                elif self.y < self.height:
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

                elif direction == "ru":
                    if self.x < self.width and self.y > 0:
                        self.x += 10
                        self.y -= 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.x < self.width:
                        self.x += 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.y > 0:
                        self.y -= 10
                        pyautogui.moveTo(self.x, self.y)

                elif direction == "rd":
                    if self.x < self.width and self.y < self.height:
                        self.x += 10
                        self.y += 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.x < self.width:
                        self.x += 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.y < self.height:
                        self.y += 10
                        pyautogui.moveTo(self.x, self.y)

                elif direction == "lu":
                    if self.x > 0 and self.y > 0:
                        self.x -= 10
                        self.y -= 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.x > 0:
                        self.x -= 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.y > 0:
                        self.y -= 10
                        pyautogui.moveTo(self.x, self.y)

                elif direction == "ld":
                    if self.x > 0 and self.y < self.height:
                        self.x -= 10
                        self.y += 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.x > 0:
                        self.x -= 10
                        pyautogui.moveTo(self.x, self.y)
                    elif self.y < self.height:
                        self.y += 10
                        pyautogui.moveTo(self.x, self.y)

                t.sleep(0.1)
                if self.stop:
                    break
