import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',category=FutureWarning)
    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    from botchart import BotChart
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import LSTM
    from keras.layers import Dropout


# Data preprocessing : scaling, reshaping
chart = BotChart('poloniex','BTC_ETH',7200,'2014-11-02 14:00:00','2016-12-14 20:53:20')
list_opens = []
for val in chart.data:
    list_opens.append(val.open)
test_size = int(0.1*len(list_opens))
opens = (np.array(list_opens)).reshape(-1,1)
scaler = MinMaxScaler(feature_range = (0,1))
opens_scaled = scaler.fit_transform(opens)
timestep = 60

x_train = []
y_train = []
for i in range(timestep,len(opens_scaled)-test_size):
    x_train.append(opens_scaled[i-timestep:i])
    y_train.append(int(opens_scaled[i] > opens_scaled[i-1]))

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

x_test = []
y_true = []
for i in range(len(opens_scaled)-test_size,len(opens_scaled)):
    x_test.append(opens_scaled[i-timestep:i])
    y_true.append(int(opens_scaled[i] > opens_scaled[i-1]))

x_test = np.array(x_test)

# Build RNN with LSTM layers
classifier = Sequential()
classifier.add(LSTM(units = 40, input_shape = (x_train.shape[1], x_train.shape[2]), return_sequences = True))
classifier.add(Dropout(0.15))
classifier.add(LSTM(units = 40, return_sequences = True))
classifier.add(Dropout(0.15))
classifier.add(LSTM(units = 40))
classifier.add(Dropout(0.15))
classifier.add(Dense(units = 1, activation = 'sigmoid'))
# classifier.add(Dropout(0.1))
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics=['accuracy'])
classifier.fit(x_train, y_train, epochs = 10, batch_size = 32)

classifier.save("classification_model.h5")

y_predict = classifier.predict(x_test)
print(y_predict)
