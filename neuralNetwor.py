import numpy as np
import pandas as pd

from keras.layers import Dense
from keras.models import Sequential, load_model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping


class NeuralNetwork:

    def __init__(self, n_input, n_output, batch_size, epochs):
        self.n_input = n_input
        self.n_output = n_output
        self.batch_size = batch_size
        self.epochs = epochs
        self.model = Sequential([
            Dense(42, input_shape=(n_input,), activation='relu'),
            Dense(42, activation='relu'),
            Dense(42, activation='relu'),
            Dense(42, activation='relu'),
            Dense(42, activation='relu'),
            Dense(n_output, activation='softmax')
        ])
        #For a multi - class classification problem
        self.model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])


    def train(self, dataset, dropDuplicate):
        print("------------------------------Training Start------------------------------")
        if dropDuplicate:
            df = pd.read_csv(dataset, names=["result", "state"])
            df = df.drop_duplicates(subset=["result", "state"])
        else:
            df = pd.read_csv(dataset)

        df = df.to_numpy()
        X = []
        y = []
        counter = 1

        for data in df:
            if counter % 50000 == 0:
                print("read {}/{} lines, {}%".format(counter, df.shape[0], round((counter/df.shape[0])*100, 2)))
            X.append(np.matrix(data[1]))
            y.append(data[0])
            counter += 1

        X = np.array(X).reshape(-1, self.n_input)
        y = to_categorical(y, num_classes=3)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("shape of input - training set", len(X_train))
        print("shape of output - training set", len(y_train))
        print("shape of input - testing set", len(X_test))
        print("shape of output - testing set", len(y_test))

        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=self.epochs, batch_size=self.batch_size, callbacks=EarlyStopping(patience=5, monitor='accuracy'))
        if dropDuplicate:
            self.model.save("modelSaved/model-" + str(dataset[8:-4]) + "_" + str(self.batch_size) + "bs_noDupl.h5")
        else:
            self.model.save("modelSaved/model-" + str(dataset[8:-4]) + "_" + str(self.batch_size) + "bs.h5")
        print("------------------------------Training End------------------------------")


    def load(self, model):
        self.model = load_model(model)
        print("Model loaded successfully")


    def predict(self, data):
        return self.model.predict(np.array(data).reshape(-1, self.n_input))