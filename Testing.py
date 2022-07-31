import random

import numpy as np
from scipy import rand
from Processing import DataReader
from Training import load_model
from Training import labels
import msvcrt as keyboard


class EEGDataGen:
    def __init__(self):
        self.global_direction = "Right"

    def randomFlag(self):
        if self.global_direction == "Right":
            self.global_direction = "Left"
            return "Left"
        else:
            self.global_direction = "Right"
            return "Right"

    def main(self):
        model = load_model()
        if model is not None:
            print("Model loaded")
        else:
            print("Model not found")
        dr = DataReader(500)
        while True:
            time_to_wait = random.randint(5, 15)
            direction = self.randomFlag()
            while time_to_wait > 0:
                time_to_wait -= 1
                # read data from get_data()
                freq, fftData, bands = dr.get_data()
                bands = np.rint(bands)
                print(bands)
                bands = bands.reshape(1, 10)
                print(bands)
                print(bands.shape)
                predictions = model.predict(bands)
                print("press " + direction)
                input_direction = (
                    "Right" if keyboard.getch().decode("utf-8") == "r" else "Left"
                )
                print("You pressed: " + input_direction)
                print(
                    "Model predicted: " + labels[np.argmax(predictions)],
                    "with probability",
                    np.amax(predictions) * 100,
                    "%",
                )


if __name__ == "__main__":

    eeg = EEGDataGen()
    eeg.main()
