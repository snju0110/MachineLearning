#sanjay
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler

dataset = pd.read_csv('Google_Stock_Price_Train.csv')
print(dataset.head())

train_set = dataset.iloc[:, 1:2].values

scaler = MinMaxScaler(feature_range=(0, 1))
scale_train_set = scaler.fit_transform(train_set)

print(scale_train_set)

X_train = []
Y_train = []

for i in range(60, 1258):
    X_train.append(scale_train_set[i - 60:i, 0])
    Y_train.append(scale_train_set[i, 0])

X_train = np.array(X_train)
Y_train = np.array(Y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

print(X_train.shape)

regressor = Sequential()

regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units=1))

regressor.compile(optimizer='adam', loss='mean_squared_error')
regressor.fit(X_train, Y_train, epochs=100, batch_size=32)

dataset_test = pd.read_csv("Google_Stock_Price_Test.csv")

actual_stock = dataset_test.iloc[:, 1:2].values

dataset_total = pd.concat((dataset['Open'], dataset_test['Open']), axis=0)

inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values

inputs = inputs.reshape(-1, 1)
inputs = scaler.transform(inputs)

X_test = []

for i in range(60, 80):
    X_test.append(inputs[i - 60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

prec_stp = regressor.predict(X_test)
prec_stp = scaler.inverse_transform(prec_stp)

plt.plot(actual_stock, color='red', label='Actual stock price')
plt.plot(prec_stp, color='black', label='forecastbstock price')
plt.title('hvtyvt')
plt.xlabel("time")
plt.ylabel('stock price')
plt.legend()
plt.show()
