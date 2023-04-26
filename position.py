from datetime import datetime


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
