import datetime


class Bar:
    def __init__(self, symbol: str, timeframe: int, open: float, high: float, low: float, close: float, volume: float, dt: datetime):
        self.symbol = symbol
        self.timeframe = timeframe
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.dt = dt
