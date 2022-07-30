import random
import time
import EEGDataGen as dataGen
import msvcrt as keyboard
import numpy as np
from Processing import DataReader
import regex as re

class csvWriter:

    def __init__(self, channels, sources) -> None:
        self.direction = "Right"
        self.frequencies = np.array([])
        self.amplitudes = np.array([])
        self.bands = np.array([])
        self.fileNameBin = ""
        self.fileNameRaw = ""
        self.dr = DataReader(1000)
        self.channels = channels
        self.sources = sources

    def intro(self):
        print("Get Ready to Focus ")
        print("Please hit the key 'R' when asked to Enter Right and 'L' for Left")
        index = 5
        while index > 0:
            t0 = time.time()
            print(index)
            while(True):
                t1 = time.time()
                if(t1-t0) > 0.5:
                    break
            index -= 1
            

    def inputLoop(self):

        endTime = time.time() + self.randomTime() 
        self.direction = self.changeFlag()
                #while true, enter the loop, have a time checker that breaks it, but while doing this if you end up 
                #out of range you need to extend the loop
        while(time.time() < endTime):
            print("\nENTER " + self.direction + "\n")
            keyboard.getch()
            self.frequencies, self.amplitudes, self.bands = self.dr.get_data()
            self.writeFileBin()
            self.writeFileRaw()

                
    def writeFileBin(self):
        size = self.channels * self.sources
        final = ""
        for i in range(size):
            final += str(self.bands[i]) # type: ignore
            final += ", "
        final += self.direction + "\n"
        file = open(self.fileNameBin, "a")
        file.write(final)    

    def writeFileRaw(self):
        size = self.sources
        final = str(self.frequencies) + ","
        for i in range(size):
            final += str(self.amplitudes[i,:]) # type: ignore
            final += ","
        final += self.direction + "\n"
        file = open(self.fileNameRaw, "a")
        file.write(final)           
        
    # def withinRange(readIn):
    #     threshold1 = 13
    #     threshold2 = 29
    #     input1Valid = readIn[0] > threshold1 and readIn[0] < threshold2
    #     input2Valid = readIn[1] > threshold1 and readIn[1] < threshold2
    #     if(input1Valid and input2Valid):
    #         return True
    #     else: 
    #         return False

    #here for test only
    def changeFlag(self):
        if(self.direction == "Left"):
            return "Right"
        else: 
            return "Left"

    def randomTime(self):
        return random.randint(2, 7)


def main():

    channels = 5
    sources = 2
    writer = csvWriter(channels, sources)
    writer.intro()
    # dr = DataReader(1000)
    focusTime = 5 * 60
    finalTime = time.time() + focusTime
    fileHeader = ",".join(writer.dr.get_names()) + ", direction\n" 
    writer.fileNameBin = dataGen.findEmptyFile("bin")
    writer.fileNameRaw = dataGen.findEmptyFile("raw")
    file = open(writer.fileNameBin, "w")
    file.write(fileHeader)
    file.close()
    

    while(time.time() < finalTime):
        
            writer.inputLoop()

if __name__ == "__main__":
    # Method call for main: This initializes and completes method calls using the UserInterface and EncryptionProcessor classes to
    # facilitate the execution of the encrytion application.
    main()
