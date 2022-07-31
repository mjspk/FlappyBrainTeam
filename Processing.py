import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from queue import Queue


class DataReader:
    def __init__(self, buffer_length):

        self.ser = serial.Serial("COM4", 115200, timeout=0.001)
        self.ser.flushInput()
        self.ser.flushOutput()

        time.sleep(5)
        self.data = Queue(buffer_length)
        self.bin_names = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.bands = [1, 2, 4, 5, 6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

    def get_data(self, plot=False):

        self.read_serial()

        # Convert the data left in the queue to a numpy array
        while not self.data.full():
            time.sleep(0.1)
            self.read_serial()

        data_array = np.array(self.data.queue)
        freq = np.fft.fftfreq(data_array.shape[0]) * np.average(data_array[0, 0])

        freq = freq[0 : len(freq) // 2]

        fftData = None
        bandsData = None

        for i in range(1, data_array.shape[1]):

            # Do a FFT on the data
            fftReading = np.fft.fft(data_array[:, i])
            fftReading = fftReading[0 : len(fftReading) // 2]
            fftReading = np.sqrt(fftReading.real**2 + fftReading.imag**2)

            if fftData is None:
                fftData = fftReading
            else:
                fftData = np.vstack((fftData, fftReading))
                # y, x = fftData.shape
                # fftData = fftData.reshape((x, y))

            bands = self.create_bands(freq, fftReading)

            if bandsData is None:
                bandsData = bands
            else:
                bandsData = np.hstack((bandsData, bands))
                # y, x = bandsData.shape
                # bandsData = bandsData.reshape((x, y))

        if plot:
            plt.plot(data_array)
            plt.stem(freq, fftReading, markerfmt=" ")
            plt.legend()
            plt.show(block=True)

        # Return results of the fourier transform
        return freq, fftData, bandsData


    def get_data2(self, plot=False):

        self.read_serial()

        # Convert the data left in the queue to a numpy array
        while not self.data.full():
            time.sleep(0.1)
            self.read_serial()

        data_array = np.array(self.data.queue)
        freq = np.fft.fftfreq(data_array.shape[0]) * np.average(data_array[0, 0])

        freq = freq[0 : len(freq) // 2]

        fftData = None
        bandsData = None

        for i in range(1, data_array.shape[1]):

            # Do a FFT on the data
            fftReading = np.fft.fft(data_array[:, i])
            fftReading = fftReading[0 : len(fftReading) // 2]
            fftReading = np.sqrt(fftReading.real**2 + fftReading.imag**2)

            if fftData is None:
                fftData = fftReading
            else:
                fftData = np.vstack((fftData, fftReading))
                # y, x = fftData.shape
                # fftData = fftData.reshape((x, y))

            bands = self.create_bands(freq, fftReading)

            if bandsData is None:
                bandsData = bands
            else:
                bandsData = np.hstack((bandsData, bands))
                # y, x = bandsData.shape
                # bandsData = bandsData.reshape((x, y))

        if plot:
            plt.plot(data_array)
            plt.stem(freq, fftReading, markerfmt=" ")
            plt.legend()
            plt.show(block=True)

        # Return results of the fourier transform
        return bandsData, data_array

    def read_serial(self):

        # Throw away top line
        self.ser.readline()

        input_raw = self.ser.readline()
        input_decoded = input_raw.decode()

        # Read in data until the end of the file
        # while len(input_decoded) > 3 and input_decoded[-3] == ">":
        while self.ser.inWaiting() > 1:

            try:
                if input_decoded[0] != "<" or input_decoded[-3] != ">":
                    input_raw = self.ser.readline()
                    input_decoded = input_raw.decode()
                    continue

                if len(input_raw) > 5:
                    input_string = (
                        input_decoded.strip().replace("<", "").replace(">", "")
                    )
                    input_s_array = input_string.split()
                    input_list = list(map(float, input_s_array))
                    input_array = np.array(input_list)

                    if len(input_array) == 3:

                        if self.data.full():
                            self.data.get()

                        self.data.put(input_array)

                    input_raw = self.ser.readline()
                    input_decoded = input_raw.decode()

            except:
                input_raw = self.ser.readline()
                input_decoded = input_raw.decode()

    def get_names(self):
        return self.bin_names

    def get_bands(self):
        return self.bands 

    def create_bands(self, frequencies, amplitudes):

        bandTotals = [0 for i in range(len(self.bands))]
        bandCounts = [0 for i in range(len(self.bands))]

        for point in range(len(frequencies)):
            for i, amplitude_limit in enumerate(self.bands):
                if frequencies[point] < amplitude_limit:
                    bandTotals[i] += amplitudes[point]
                    bandCounts[i] += 1
                    break

        band_average = list(np.array(bandTotals) / np.array(bandCounts))

        return band_average

    def left_right_input(self):

        bands, data_array = self.get_data2()

        if (np.average(bands[1:4]) > 750):

            LR_data = data_array[:,1]

            if np.argmin(LR_data) < np.argmax(LR_data):
                return "right"
            else:
                return "left"

        return None



def plot_bands(bands, bin_names):
    plt.ylabel("Amplitude")
    plt.bar(bin_names, bands, color="#7967e1")
    plt.show()
    plt.clf()


def main():

    # Create Data reader with a queue length
    dr = DataReader(100)

    bin_names = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    bin_range = [4, 8, 12, 30, 100]

    plt.ion()

    # frequencies, amplitudes, bands = dr.get_data()
    # bar = ax.bar(bin_names, bands, color="#7967e1")

    # plt.show(block=False)
    ax = plt.gca()
    plt.ylabel("Amplitude")

    ind = np.arange(5)
    width = 0.35

    print("Recording")

    frequencies, amplitudes, bands = dr.get_data()
    b = dr.get_bands()

    max_y = 100


    while True:

        bands, data_array = dr.get_data2()

        # y, x = bands.shape
        # bands = bands.reshape((x, y))
        # bin_names

        isInput = dr.left_right_input()

        if isInput:
            print(isInput)
            plt.plot(data_array[:,1])
            plt.show(block = False)
        

        # max_y = max(max_y, max(bands[1:len(bands)]))


            

        
        # plt.cla()
        # plt.ylim([0,max_y])
        # plt.bar(b[1:], bands[1:len(bands)//2], color="#7967e1")

        # # bar = plt.bar(ind + width, bands[5:], width, color="green")

        # # plt.xticks(ind + width / 2, bin_names)

        plt.pause(0.01)
        time.sleep(1.25)

    # plt.stem(freq, fftData, markerfmt=" ",)
    # print(1000 / np.average(array[:,0]))
    # # plt.stem(freq, array[:,1])
    # print(array.shape)
    # # print(freq.size)
    # plt.show()


if __name__ == "__main__":
    main()
