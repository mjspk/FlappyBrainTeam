import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from queue import Queue


class DataReader:
    """
    This class reads data from the serial port and analyzes it to identify the most recent input when prompted by another file
    """

    def __init__(self):
        """
        Initialize serial port and datastructure, establish bin intervals for frequency response
        """

        self.ser = serial.Serial("COM7", 115200, timeout=0.00001)

        self.ser.flushInput()
        self.ser.flushOutput()

        time.sleep(5)
        self.data = Queue(80)
        self.bin_names = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.bands = [1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,]

    def get_data(self, plot=False):
        """
        Method calls for data from the serial port, analyzes it with a FFT and bins the data. 
        The binned data can be returned, and a plot of the data from the FFT can be shown if plot is set to true
        
        """

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

    def get_direction(self, plot=False):
        """
        This method determines the direction of the last input based on the recent readings from the serial port
        The return is a string indicating which direction to move the cursor and the binned data that is based on 
        which can later be used for a machine learning algorithm
        """

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
        """
        This method reads the serial input and updates the data queue. It filters out invalid data and leave the most recent data on the queue
        """

        # Throw away top line
        self.ser.readline()

        input_raw = self.ser.readline()
        input_decoded = input_raw.decode()

        last = [0, 0, 0]

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

                        last = input_array
                        self.data.put(input_array)

                    input_raw = self.ser.readline()
                    input_decoded = input_raw.decode()

            except:
                input_raw = self.ser.readline()
                input_decoded = input_raw.decode()

        if last[1] < 450 or last[1] > 550 or last[-1] < 450 or last[-1] > 550:
            time.sleep(0.1)
            self.read_serial()

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

    def compute_input(self):

        bands, data_array = self.get_direction()

        l = len(bands)
        side_data = np.average(bands[1:4])
        vert_data = np.average(bands[l // 2 + 1 : l // 2 + 4])

        if side_data < 800 and vert_data < 600:
            return None, bands

        print(f"Side Sensors: {side_data}, Vertical Sensors {vert_data}")

        if side_data > 900:
            # look for a side to side input
            LR_data = data_array[:, 1]

            if ((np.average(LR_data) - np.min(LR_data)) > 1.8 * (np.max(LR_data) - np.average(LR_data))):
                return "b", bands

            if np.argmin(LR_data) < np.argmax(LR_data):
                return "r", bands
            else:
                return "l", bands

        else:
            # look for a vertical input
            UD_data = data_array[:, 2]

            if np.argmin(UD_data) < np.argmax(UD_data):

                if np.max(UD_data) < 650:
                    return "b", bands
                else:
                    return "u", bands
            else:
                return "d", bands


def plot_bands(bands, bin_names):
    """
    This method plots a histagram showing the results of a fourier transform after binning
    """
    plt.ylabel("Amplitude")
    plt.bar(bin_names, bands, color="#7967e1")
    plt.show()
    plt.clf()


def main():
    """
    Main function for testing the DataReader class
    """
    

    # Create Data reader with a queue length
    dr = DataReader()

    plt.ion()

    print("Start Reading")

    while True:

        bands, data_array = dr.get_direction()

        isInput, bands = dr.compute_input()

        if isInput:
            print(isInput)
            plt.cla()
            plt.plot(data_array[:, 1])
            plt.plot(data_array[:, 2])
            plt.show(block=False)

        plt.pause(0.01)
        time.sleep(1)

if __name__ == "__main__":
    main()
