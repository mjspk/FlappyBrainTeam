import tensorflow as tf
import pandas as pd
import numpy as np
import os
from tensorflow import keras
from keras import layers
from sklearn.preprocessing import StandardScaler, scale


labels = ["left", "right"]
# load data from csv file
def load_data(filename):
    if os.path.isfile(filename):
        data = pd.read_csv(filename)
        data.iloc[:, -1] = data.iloc[:, -1].map({"left": 0, "right": 1})
        return data
    else:
        print("File not found")
        return None


# split data into train,aval and test
def split_data(data):
    if data is not None:
        x_train = data.iloc[0 : int(len(data) * 0.8), :-1]
        y_train = data.iloc[0 : int(len(data) * 0.8), -1]
        x_val = data.iloc[int(len(data) * 0.8) : int(len(data) * 0.9), :-1]
        y_val = data.iloc[int(len(data) * 0.8) : int(len(data) * 0.9), -1]
        x_test = data.iloc[int(len(data) * 0.9) :, :-1]
        y_test = data.iloc[int(len(data) * 0.9) :, -1]
        scaler=StandardScaler()
        scaler.fit(x_train)
        x_train=scaler.transform(x_train)
        x_val=scaler.transform(x_val)
        print(x_train)
        print(x_val)
        

        return x_train, y_train, x_val, y_val, x_test, y_test

    else:
        print("Data not found")
        return None


def create_model():
    inputs = keras.Input(shape=(5,), name="digits")
    x = layers.Dense(64, activation="relu", name="dense_1")(inputs)
    # x = layers.Dense(128, activation="relu", name="dense_2")(x)
    # x = layers.Dense(256, activation="relu", name="dense_3")(x)
    outputs = layers.Dense(3, activation="softmax", name="predictions")(x)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(lr=0.001),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=[keras.metrics.SparseCategoricalAccuracy()],
    )
    return model


def train_model(model, x_train, y_train, x_val, y_val):
    if (
        model is not None
        and x_train is not None
        and y_train is not None
        and x_val is not None
        and y_val is not None
    ):
        model.fit(
            x_train,
            y_train,
            epochs=100,
            validation_data=(x_val, y_val),
            batch_size=64,
            verbose=2,
        )
        return model
    else:
        print("Model or data not found")
        return None


def evaluate_model(model, x_val, y_val):

    if model is not None and x_val is not None and y_val is not None:
        loss, acc = model.evaluate(x_val, y_val, verbose=2, batch_size=64)
        print("Accuracy: %f" % acc)
        print("Loss: %f" % loss)

    else:
        print("Model or data not found")
        return None


def predicte(model, x_test, y_test):

    if model is not None and x_test is not None and y_test is not None:
        predictions = model.predict(x_test)
        pred_y = []
        for i in predictions:
            pred_y.append(labels[np.argmax(i)] + " " + str(i[np.argmax(i)]))
        real_y = []
        y = np.array(y_test)
        for i in y:
            real_y.append(labels[i])
        print("real y, predicted y, probability")
        for i in range(len(real_y)):
            print(real_y[i], pred_y[i])

    else:
        print("Model or data not found")
        return None


def save_model(model, filename="EEGmodel.h5"):
    model.save(filename)
    print("Model saved")


def load_model(filename="EEGmodel.h5"):
    if os.path.isfile(filename):
        model = tf.keras.models.load_model(filename)
        return model
    else:
        return None


if __name__ == "__main__":
    data = load_data("BatchTestCSVData2.csv")
    x_train, y_train, x_val, y_val, x_test, y_test = split_data(data)
    model = load_model()
    if model is None:
        model = create_model()
        model = train_model(model, x_train, y_train, x_val, y_val)
    evaluate_model(model, x_val, y_val)
    predicte(model, x_test, y_test)
