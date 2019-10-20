from strategies.botstrategy import BotStrategy
from botposition import BotPosition
import numpy as np
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',category=FutureWarning)
    from keras import models

# Strategy based on LSTM neural network which predicts the next closing price
class SLSTM(BotStrategy):
    def __init__(self):
        super(SLSTM,self).__init__()
        self.model = models.load_model('regression_model.h5')
        self.timestep = 60 # it MUST be the timestep used for lstm training
        self.wait = 0

    # Open a short or long position depending on the model prediction, waiting for 10 candelstick between two positions.
    def open_position(self,candlestick):
        if len(self.prices) > self.timestep and self.wait > 50:
            self.wait = 0
            array = np.array(self.prices[-self.timestep:])
            x_input = np.reshape(array, (1,array.shape[0],1))
            predicted = self.model.predict(x_input)
            predicted = predicted[0][0]
            if predicted > self.prices[-1]:
                return BotPosition(self.current_price,candlestick.start_time,short = False)
            else:
                return BotPosition(self.current_price,candlestick.start_time,short = True)
        self.wait += 1
        return None


    # We trust the model so when the next candlestick comes we close the position
    def try_close_position(self,position, candlestick):
        position.close(self.current_price,candlestick.start_time)
