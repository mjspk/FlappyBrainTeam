from random import randint

"""
So below is the final script i'll be working with. I've chosen to concatenate my values and then stream them to a file
which i'll then be able to upload to AMLS. I chose a range of 30s to simulate 30 seconds of test data per word. This 
imaginery user has had 10 training sessions with each word.
"""
# EEG Ranges
# S:000|D:0.5-2.75|T:3.5-6.75|LA:7.5-9.25|HA:10-11.75|LB:13-16.75|HB:18-29.75|LG:31-39.75|MG:41-49.75;

# FULL
def generateFull(word):
    global main
    main = ""
    for i in range(0, 300):
        lG = randint(3100, 3975)
        hG = randint(4100, 4975)
        main += "{0},{1},{2}".format(lG, hG, word) + "\n"
    return main


# LOW
def generateLow(word):
    global main
    main = ""
    for i in range(0, 300):
        lG = randint(3100, 3300)
        hG = randint(4100, 4500)
        main += "{0},{1},{2}".format(lG, hG, word) + "\n"
    return main


# HIGH
def generateHigh(word):
    global main
    main = ""
    for i in range(0, 300):
        lG = randint(3500, 3975)
        hG = randint(4600, 4975)
        main += "{0},{1},{2}".format(lG, hG, word) + "\n"

    return main


def findEmptyFile(type):
    try:
        found = False
        index = 0
        while found == False:
            fileName = type + str(index) + ".csv"
            file = open(fileName, "r")
            if file.read() == "":
                found = True
            index = index + 1
    except IOError:
        found = True
    return type + str(index) + ".csv"


# COMMANDS
times = 10
final = "Signal1,Signal1,Word" + "\n"
for i in range(0, times):
    # generateFull("test")
    final += generateLow("left")
    final += generateHigh("right")
fileName = findEmptyFile("BatchTestCSVData")
file = open(fileName, "w")
file.write(final)
