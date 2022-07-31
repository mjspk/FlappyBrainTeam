import random
import time
import EEGDataGen as dataGen
import msvcrt as keyboard
import numpy as np
from Processing import DataReader


class CSVDataReader:
    def __init__(self):
        self.globle_direction = "Right"
        self.fileName = ""

    def intro(self):
        print("Get Ready to Focus ")
        print("Please hit the key 'R' when asked to Enter Right and 'L' for Left")
        index = 5
        while index > 0:
            t0 = time.time()
            print(index)
            while True:
                t1 = time.time()
                if (t1 - t0) > 1:
                    break
            index -= 1

    def inputLoop(self, dr, fileNameBin, fileNameRaw):

        endTime = time.time() + self.randomTime()
        direction = self.randomFlag()
        # while true, enter the loop, have a time checker that breaks it, but while doing this if you end up
        # out of range you need to extend the loop
        while time.time() < endTime:
            readIn = [0, 0, 0]
            print("\nENTER " + direction + "\n")
            keyboard.getch()
            readIn[0], readIn[1], readIn[2] = dr.get_data()
            self.writeFileBin(direction, fileNameBin, readIn)
            self.writeFileRaw(direction, fileNameRaw, readIn)

    def writeFileBin(self, direction, fileName, readIn):
        size = 10

        final = ""
        for i in range(size):
            final += str(round(readIn[2][i]))
            final += ","
        final += direction + "\n"
        file = open(fileName, "a")
        file.write(final)

    def writeFileRaw(self, direction, fileName, readIn):
        size = 4
        final = str(readIn[0]) + ","
        for i in range(size):
            final += str(readIn[1][i, :])  # type: ignore
            final += ","
        final += direction + "\n"
        file = open(fileName, "a")
        file.write(final)

    def withinRange(self, readIn):
        threshold1 = 13
        threshold2 = 29
        input1Valid = readIn[0] > threshold1 and readIn[0] < threshold2
        input2Valid = readIn[1] > threshold1 and readIn[1] < threshold2
        if input1Valid and input2Valid:
            return True
        else:
            return False

    # here for test only
    def randomFlag(self):
        if self.globle_direction == "Right":
            self.globle_direction = "Left"
            return "Left"
        elif self.globle_direction == "Left":
            self.globle_direction = "Up"
            return "Up"
        elif self.globle_direction == "Up":
            self.globle_direction = "Down"
            return "Down"
        elif self.globle_direction == "Down":
            self.globle_direction = "Blink"
            return "Blink"
        else:
            self.globle_direction = "Right"
            return "Right"

    def randomTime(self):
        # return random.randint(2, 5)
        return 10

    #New function
    def makeHeader(self):
        fileHeader = "DeltaRight,ThetaRight,AlphaRight,BetaRight,GammaRight,DeltaLeft,ThetaLeft,AlphaLeft,BetaLeft,GammaLeft,Direction\n"
        self.fileNameBin = dataGen.findEmptyFile("bin")
        file = open(self.fileNameBin, "w")
        file.write(fileHeader)
        file.close()
    
    #New function
    def writeFile(self, direction, bands):
        size = 4
        final = ""
        for i in range(size):
            final += str(bands[i]) # type: ignore
            final += ","
        final += direction + "\n"
        file = open(self.fileNameBin, "a")
        file.write(final)    

    def main(self):

        dr = DataReader(500)
        focusTime = 0.25 * 60
        finalTime = time.time() + focusTime
        fileHeader = "DeltaRight,ThetaRight,AlphaRight,BetaRight,GammaRight,DeltaLeft,ThetaLeft,AlphaLeft,BetaLeft,GammaLeft,Direction\n"
        fileNameBin = dataGen.findEmptyFile("bin")
        fileNameRaw = dataGen.findEmptyFile("raw")
        file = open(fileNameBin, "w")
        file.write(fileHeader)
        file.close()
        self.intro()

        while time.time() < finalTime:

            self.inputLoop(dr, fileNameBin, fileNameRaw)


if __name__ == "__main__":
    # Method call for main: This initializes and completes method calls using the UserInterface and EncryptionProcessor classes to
    # facilitate the execution of the encrytion application.
    dr = CSVDataReader()
    dr.main()