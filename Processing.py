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
        self.bin_names = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]

    def get_data(self, plot = False):
        
        # data = np.array([[2,2],[2,2]])
        
        # Throw away top line
        self.ser.readline()

        input_raw = self.ser.readline()
        input_decoded = input_raw.decode()

        # Read in data until the end of the file
        while (len(input_decoded) > 3 and input_decoded[-3] == ">"):

            if len(input_raw) > 5:
                input_string  = input_decoded.strip().replace("<","").replace(">","")
                input_s_array = input_string.split()
                input_list    = list(map(float, input_s_array))
                input_array = np.array(input_list)

                if self.data.full():
                    self.data.get()

                self.data.put(input_array)
                # data = np.append(data, input_array.reshape((1,2)), axis = 0)

                input_raw = self.ser.readline()
                input_decoded = input_raw.decode()

        # Convert the data left in teh queue to a numpy array
        data_array = np.array(self.data.queue)

        # Do a FFT on the data
        fftData = np.fft.fft(data_array[:,1])
        fftData = np.sqrt(fftData.real**2 + fftData.imag**2)
        freq = np.fft.fftfreq(data_array.shape[0]) * np.average(data_array[:,0])

        fftData = fftData[0:len(fftData)//2]
        freq = freq[0:len(freq)//2]

        if plot:
            plt.stem(freq, fftData, markerfmt=" ")
            plt.show(block = True)

        # Return results of the fourier transform
        return freq, fftData

    def get_names(self):
        return self.bin_names

def create_bands(frequencies, amplitudes, bands):

    bandTotals = [0 for i in range(len(bands))]
    bandCounts = [0 for i in range(len(bands))]
        
    for point in range(len(frequencies)):
        for i, amplitude_limit in enumerate(bands):
            if(frequencies[point] < amplitude_limit):
                bandTotals[i] += amplitudes[point]
                bandCounts[i] += 1
                break

    bands = list(np.array(bandTotals)/np.array(bandCounts))

    return bands


def plot_bands(bands, bin_names):
    plt.ylabel("Amplitude")
    plt.bar(bin_names, bands, color="#7967e1")
    plt.show()
    plt.clf()

if __name__ == "__main__":

    # Create Data reader with a queue length
    dr = DataReader(200)

    # Give it a bit of time for the data to accumulate
    time.sleep(10)

    bin_names = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    bin_range = [4, 8, 12, 30, 100]

    plt.ion()


    
    frequencies, amplitudes = dr.get_data()
    bands = create_bands(frequencies, amplitudes, bin_range)
    # bar = ax.bar(bin_names, bands, color="#7967e1")
    
    plt.show(block = False)
    ax = plt.gca()
    plt.ylabel("Amplitude")
    max_y = 0

    frequencies, amplitudes = dr.get_data()

    while True:

        frequencies, amplitudes = dr.get_data()

        bands = create_bands(frequencies, amplitudes, bin_range)

        plt.cla()
        bar = plt.bar(bin_names, bands, color="#7967e1")

        max_y = max(max_y, max(bands))
        ax.set_ylim([0,max_y])

        print(f"Bands: {bands} + Total Length: {amplitudes.shape}")
        
        plt.pause(0.01)
        time.sleep(1)

    # plt.stem(freq, fftData, markerfmt=" ",)
    # print(1000 / np.average(array[:,0]))
    # # plt.stem(freq, array[:,1])
    # print(array.shape)
    # # print(freq.size)
    # plt.show()
