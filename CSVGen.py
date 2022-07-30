
import random
import time
import EEGDataGen as dataGen
import msvcrt

def intro(direction):
    print("Get Ready to Focus on " + direction)
    index = 5
    while index > 0:
        t0 = time.time()
        print(index)
        while(True):
            t1 = time.time()
            if(t1-t0) > 1:
                break
        index -= 1
        

def inputLoop(direction, focusTime, readIn, fileName):
    endTime = time.time() + focusTime 
            #while true, enter the loop, have a time checker that breaks it, but while doing this if you end up 
            #out of range you need to extend the loop
    while(time.time() < endTime):
        print("\nENTER " + direction + "\n")
        msvcrt.getch()
        writeFile(direction, fileName, readIn)
        readIn = randomInput()
        if not withinRange(readIn):
            endTime = pause(time.time(), endTime, readIn)
            
def writeFile(direction, fileName, readIn):
    final = "{0},{1},{2}".format(readIn[0], readIn[1], direction) + "\n"
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

def pause(pauseTime, endTime, readIn):
    while not withinRange(readIn):
        readIn = randomInput()
    return time.time() + endTime - pauseTime

#here for test only
def randomInput():
    
    return random.randint(15, 29), random.randint(15,29)

def main():

    
    readIn = [15, 20] #get input from file
    focusTime = 10
    readIn[0], readIn[1] = randomInput()
    fileHeader = "Signal1,Signal1,Word" + "\n" 
    fileName = dataGen.findEmptyFile("output")
    file = open(fileName, "w")
    file.write(fileHeader)
    file.close()
    
    while(True):
        
        readIn[0], readIn[1] = randomInput() 

        if(withinRange(readIn)):
            direction = "Right"
            intro(direction)
            inputLoop(direction, focusTime, readIn, fileName)
            direction = "Left"
            intro(direction)
            inputLoop(direction, focusTime, readIn, fileName)
            exit()
                



            






if __name__ == '__main__':
    # Method call for main: This initializes and completes method calls using the UserInterface and EncryptionProcessor classes to
    # facilitate the execution of the encrytion application.
    main()
