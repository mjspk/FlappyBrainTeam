
import random
import time
import EEGDataGen as dataGen
import msvcrt as keyboard
import numpy as np
from Processing import DataReader

def intro():
    print("Get Ready to Focus ")
    print("Please hit the key 'R' when asked to Enter Right and 'L' for Left")
    index = 5
    while index > 0:
        t0 = time.time()
        print(index)
        while(True):
            t1 = time.time()
            if(t1-t0) > 1:
                break
        index -= 1
        

def inputLoop(dr, fileNameBin, fileNameRaw):

    endTime = time.time() + randomTime() 
    direction = randomFlag()
            #while true, enter the loop, have a time checker that breaks it, but while doing this if you end up 
            #out of range you need to extend the loop
    while(time.time() < endTime):
        readIn = []
        print("\nENTER " + direction + "\n")
        keyboard.getch()
        readIn[0], readIn[1], readIn[2] = dr.get_data()
        writeFileBin(direction, fileNameBin, readIn)
        writeFileRaw(direction, fileNameRaw, readIn)

            
def writeFileBin(direction, fileName, readIn):
    size = np.shape(readIn[2])[1]
    final = ""
    for i in range(size):
        final += str(readIn[:,i])[1:-1]
        final += ", "
    final += direction + "\n"
    file = open(fileName, "a")
    file.write(final)    

def writeFileRaw(direction, fileName, readIn):
    final  = direction + ", "
    final += np.vstack([readIn[0], readIn[1]]) + "\n"
    file = open(fileName, "a")
    file.write(final)        
    
def withinRange(readIn):
    threshold1 = 13
    threshold2 = 29
    input1Valid = readIn[0] > threshold1 and readIn[0] < threshold2
    input2Valid = readIn[1] > threshold1 and readIn[1] < threshold2
    if(input1Valid and input2Valid):
        return True
    else: 
        return False

#here for test only
def randomFlag():
    newFlag = random.randint(0, 1)
    if(newFlag == 0):
        return "Right"
    else: 
        return "Left"

def randomTime():
    return random.randint(5, 15)

def main():

    
    dr = DataReader(1000)
    focusTime = 5 * 60
    finalTime = time.time() + focusTime
    fileHeader = ",".join(dr.get_names()) + ", direction\n" 
    fileNameBin = dataGen.findEmptyFile("bin")
    fileNameRaw = dataGen.findEmptyFile("raw")
    file = open(fileNameRaw, "w")
    file.write(fileHeader)
    file.close()
    intro()

    while(time.time() < finalTime):
        
            inputLoop(dr, fileNameBin, fileNameRaw)

                



            






if __name__ == '__main__':
    # Method call for main: This initializes and completes method calls using the UserInterface and EncryptionProcessor classes to
    # facilitate the execution of the encrytion application.
    main()
