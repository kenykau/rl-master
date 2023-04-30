from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

class Position:
    def __init__(self, symbol: str, lots: int, closed_date_time: str, closed: bool, open_price: float, closed_price: float,
                 open_date_time: str, closed_profit: float, max_floating_loss: float, max_floating_profit: float,
                 holding_bars: int, current_pnl: float):
        self.symbol = symbol
        self.lots = lots
        self.closed_date_time = datetime.strptime(
            closed_date_time, '%Y-%m-%d %H:%M:%S')
        self.closed = closed
        self.open_price = open_price
        self.closed_price = closed_price
        self.open_date_time = datetime.strptime(
            open_date_time, '%Y-%m-%d %H:%M:%S')
        self.closed_profit = closed_profit
        self.max_floating_loss = max_floating_loss
        self.max_floating_profit = max_floating_profit
        self.holding_bars = holding_bars
        self.current_pnl = current_pnl

def CheckFractal(instrument, i, price_type):
    result = False
    j = i - 2
    
    if price_type == 'High':
        if (instrument.historical_data['High'][i] > instrument.historical_data['High'][i+1] and
            instrument.historical_data['High'][i] > instrument.historical_data['High'][i+2] and
            instrument.historical_data['High'][i] > instrument.historical_data['High'][i-1] and
            instrument.historical_data['High'][i] > instrument.historical_data['High'][i-2]):
            result = True

    if price_type == 'Low':
        if (instrument.historical_data['Low'][i] < instrument.historical_data['Low'][i+1] and
            instrument.historical_data['Low'][i] < instrument.historical_data['Low'][i+2] and
            instrument.historical_data['Low'][i] < instrument.historical_data['Low'][i-1] and
            instrument.historical_data['Low'][i] < instrument.historical_data['Low'][i-2]):
            result = True
            
    return j if result else None


def Compute(instrument, i, n):
    uppers = []
    lowers = []

    while len(uppers) < n or len(lowers) < n:
        j_high = CheckFractal(instrument, i, 'High')
        j_low = CheckFractal(instrument, i, 'Low')
        
        if j_high is not None:
            uppers.append(j_high)
        if j_low is not None:
            lowers.append(j_low)
        
        i -= 1

    def compute_regression_line(indices, price_type):
        x = np.array(indices).reshape(-1, 1)
        y = instrument.historical_data[price_type].iloc[indices].values.reshape(-1, 1)
        model = LinearRegression().fit(x, y)
        return model.coef_[0][0], model.intercept
