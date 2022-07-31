import random
import time
import mouse as m
import numpy as np
from Controling import Controling
from Processing import DataReader
from Training import load_model
from Training import labels
import msvcrt as keyboard


class EEGDataGen:
    def main(self):

        model = load_model()
        cn = Controling(960, 540)
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
        cn = Controling(960, 540)

        dr = DataReader(75)
        while True:
            direction = dr.left_right_input()
            if direction is not None:
                cn.move_mouse(direction)
                print("Predicted: " + direction)
            else:
                print("No direction")
            time.sleep(1)


if __name__ == "__main__":

    eeg = EEGDataGen()
    eeg.test()
