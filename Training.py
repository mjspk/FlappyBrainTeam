import tensorflow as tf
import pandas as pd
import numpy as np
import os
from tensorflow import keras
from keras import layers
from sklearn.preprocessing import StandardScaler, scale
from tensorflow import feature_column


labels = ["left", "right", "backward", "forward"]
# loop all csv files in the folder data/bin and create a dataframe
def load_data():
    data = None
    for filename in os.listdir("data/bin"):
        if filename.endswith(".csv"):
            if data is None:
                data = pd.read_csv("data/bin/" + filename)
            else:
                data = data.append(pd.read_csv("data/bin/" + filename))
    data.iloc[:, -1] = data.iloc[:, -1].map(
        {"Left": 0, "Right": 1, "Backward": 2, "Forward": 3}
    )

    data = data.drop(columns=["GammaRight", "GammaLeft"])
    return data


def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop("Direction")
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds


# split data into train,aval and test df
def split_data(data):
    if data is not None:
        train_df = data.sample(frac=0.8, random_state=0)
        val_df = data.drop(train_df.index)
        test_df = val_df.sample(frac=0.5, random_state=0)
        val_df = val_df.drop(test_df.index)
        return train_df, val_df, test_df

    else:
        print("Data not found")
        return None


def create_model(feature_columns):
    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
    model = tf.keras.Sequential(
        [
            feature_layer,
            layers.Dense(128, activation="relu"),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.1),
            layers.Dense(1),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    return model


def train_model(model, train_ds, val_ds):
    if model is not None and train_ds is not None and val_ds is not None:
        model.fit(train_ds, validation_data=val_ds, epochs=10)
        return model
    else:
        print("Model or data not found")
        return None


def evaluate_model(model, val_ds):

    if model is not None and val_ds is not None:
        loss, acc = model.evaluate(val_ds)
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
    data = load_data()
    train_df, val_df, test_df = split_data(data)
    train_ds = df_to_dataset(train_df)
    val_ds = df_to_dataset(val_df, shuffle=False)
    test_ds = df_to_dataset(test_df, shuffle=False)
    for feature_batch, label_batch in train_ds.take(1):
        print("Every feature:", list(feature_batch.keys()))
        print("A batch of targets:", label_batch)
    feature_columns = []
    indicator_column_names = "DeltaRight,ThetaRight,AlphaRight,BetaRight,DeltaLeft,ThetaLeft,AlphaLeft,BetaLeft"
    for col_name in indicator_column_names.split(","):
        categorical_column = feature_column.categorical_column_with_vocabulary_list(
            col_name, data[col_name].unique()
        )
        indicator_column = feature_column.indicator_column(categorical_column)
        feature_columns.append(indicator_column)
    model = load_model()
    if model is None:
        model = create_model(feature_columns)
        model = train_model(model, train_ds, val_ds)
        evaluate_model(model, test_ds)
        # save_model(model)
