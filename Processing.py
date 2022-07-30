import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from queue import Queue

class DataReader():

    def __init__(self, buffer_length):
        self.ser = serial.Serial("COM4", 9600, timeout = .001)
        time.sleep(1)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.data = Queue(buffer_length)

    def get_data(self):
        
        data = np.array([[2,2],[2,2]])
        
        # Throw away top line
        self.ser.readline()

        input_raw = self.ser.readline()
        input_decoded = input_raw.decode()

        while (len(input_decoded) > 3 and input_decoded[-3] == ">"):

            if len(input_raw) > 5:
                input_string  = input_decoded.strip().replace("<","").replace(">","")
                input_s_array = input_string.split()
                input_list    = list(map(float, input_s_array))
                input_array = np.array(input_list)

                data = np.append(data, input_array.reshape((1,2)), axis = 0)

                input_raw = self.ser.readline()
                input_decoded = input_raw.decode()

        data = data[2:,:]
        
        return data

    def plotBands(self, bands):
        binNames = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
        plt.ylabel("Amplitude")
        plt.bar(binNames, bands, color="#7967e1")
        plt.show()
        plt.clf()

if __name__ == "__main__":

    dr = DataReader()

    array = dr.get_data()

    # print(array[1,:].shape[0])
    fftData = np.fft.fft(array[:,1])
    fftData = np.sqrt(fftData.real**2 + fftData.imag**2)
    # print(fftData)

    freq = np.fft.fftfreq(array.shape[0]) *75 #* (1000/np.average(array[:,0]))

    bandTotals = [0,0,0,0,0]
    bandCounts = [0,0,0,0,0]
        
    for point in range(len(freq)):
        if(freq[point] < 4):
            bandTotals[0] += fftData[point]
            bandCounts[0] += 1
        elif(freq[point] < 8):
            bandTotals[1] += fftData[point]
            bandCounts[1] += 1
        elif(freq[point] < 12):
            bandTotals[2] += fftData[point]
            bandCounts[2] += 1
        elif(freq[point] < 30):
            bandTotals[3] += fftData[point]
            bandCounts[3] += 1
        elif(freq[point] < 100):
            bandTotals[4] += fftData[point]
            bandCounts[4] += 1

    
    bands = list(np.array(bandTotals)/np.array(bandCounts))

    print(bands)
    plotBands(bands)

    # plt.stem(freq, fftData, markerfmt=" ",)
    # print(1000 / np.average(array[:,0]))
    # # plt.stem(freq, array[:,1])
    # print(array.shape)
    # # print(freq.size)
    # plt.show()
