import random
import time
import numpy as np
from CSVGen import CSVDataReader
from Controling import Controling
from Processing import DataReader
from Training import load_model
from Training import labels
import msvcrt as keyboard
import pyautogui as pyautogui


class EEGDataGen:
    """
    This class tests the program by calling for data from the DataReader class and telling the Controlling class to move the mouse
    """

    def Model_test(self):
        """
        Method to test the ai model agains the filtered output
        """

        model = load_model()
        cn = Controling()
        if model is not None:
            print("Model loaded")
        else:
            print("Model not found")
        dr = DataReader()
        while True:
            freq, fftData, bands = dr.get_data()
            bands = np.rint(bands)
            print(bands)
            bands = bands.reshape(1, 10)
            print(bands)
            print(bands.shape)
            predictions = model.predict(bands)
            predicted_direction = labels[np.argmax(predictions)]
            print(
                "Model predicted: " + predicted_direction,
                "with probability",
                np.amax(predictions) * 100,
                "%",
            )
            cn.move_mouse(predicted_direction, 0.5)

    def test(self):
        """
        Method to test the program reading data from the serial port and moving the mouse around the screen
        """
        cn = Controling()
        cs = CSVDataReader()
        cs.makeHeader()
        dr = DataReader()
        pyautogui.FAILSAFE = False
        while True:
            direction, bands = dr.compute_input()
            if direction is not None:
                cn.move_mouse(direction)
                cs.writeFile(direction, bands)
                print("Predicted: " + direction)
            else:
                print("No direction")
            time.sleep(1)


if __name__ == "__main__":

    eeg = EEGDataGen()
    eeg.test()
