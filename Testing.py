from os import pread
from pkgutil import get_data
from time import time
from urllib.request import ProxyBasicAuthHandler

import numpy as np
from scipy import rand
from scipy.fftpack import fftfreq
from Training import load_model, predicte
from Training import labels


if "__name__" == "__main__":
    model = load_model()
    if model is not None:
        print("Model loaded")
    else:
        print("Model not found")

    while True:

        direction = rand.randint(0, 1)
        # loop for random time between 5 and 15 seconds
        time_to_wait = rand.randint(5, 15)
        while time_to_wait > 0:
            time_to_wait -= 1
            # read data from get_data()
            freq, fftData, bands = get_data()
            predictions = model.predict(bands)

            print()
            input_direction = input("press R" if direction == 0 else "Press L")
            choosen_direction = "R" if direction == 0 else "L"
            print("You pressed: " + choosen_direction)
            print(
                "Model predicted: " + labels[np.argmax(predictions)],
                "probability: ",
                predictions[np.argmax(predictions)],
            )
