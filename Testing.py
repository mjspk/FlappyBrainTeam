import random
import time
import mouse as m
import numpy as np
from CSVGen import CSVDataReader
from Controling import Controling
from Processing import DataReader
from Training import load_model
from Training import labels
import msvcrt as keyboard


class EEGDataGen:
    def Model_test(self):

        model = load_model()
        cn = Controling()
        if model is not None:
            print("Model loaded")
        else:
            print("Model not found")
        dr = DataReader(500)
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
        cn = Controling()
        cs = CSVDataReader()
        cs.makeHeader()
        dr = DataReader(75)
        while True:
            direction, bands = dr.left_right_input()
            if direction is not None:
                cn.move_mouse(direction)
                cs.writeFile(direction, bands)
                print("Predicted: " + direction)
            else:
                print("No direction")
            time.sleep(1.4)


if __name__ == "__main__":

    eeg = EEGDataGen()
    eeg.test()
