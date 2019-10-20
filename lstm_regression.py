
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',category=FutureWarning)
    import numpy as np
    from botchart import BotChart
    from keras.models import load_model
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import LSTM
    from keras.layers import Dropout
    import matplotlib
    import matplotlib.pyplot as plt

# Data preprocessing : scaling, reshaping
chart = BotChart('poloniex','BTC_ETH',7200,'2014-11-02 14:00:00','2016-12-14 20:53:20')
list_opens = []
list
for val in chart.data:
    list_opens.append(val.open)
test_size = int(0.1*len(list_opens))
opens = (np.array(list_opens)).reshape(-1,1)
timestep = 60

x_train = []
y_train = []
for i in range(timestep,len(opens)-test_size):
    x_train.append(opens[i-timestep:i])
    y_train.append(opens[i])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

x_test = []
y_true = []
for i in range(len(opens)-test_size,len(opens)):
    x_test.append(opens[i-timestep:i])
    y_true.append(opens[i])

x_test = np.array(x_test)


# Build RNN with LSTM layers
model = Sequential()
model.add(LSTM(units = 40, input_shape = (x_train.shape[1], x_train.shape[2]), return_sequences = True))
model.add(Dropout(0.15))
model.add(LSTM(units = 40, return_sequences = True))
model.add(Dropout(0.15))
model.add(LSTM(units = 40))
model.add(Dropout(0.15))
model.add(Dense(units = 1))
model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.fit(x_train, y_train, epochs = 10 , batch_size = 32)
model.save("regression_model.h5")

y_predict = model.predict(x_test)
# model.evaluate()
x = [ i for i in range(len(y_true))]
for k in range(0,len(x),10):
    plt.axvline(x=k)
plt.plot(y_true)
plt.plot(y_predict)
plt.show()
