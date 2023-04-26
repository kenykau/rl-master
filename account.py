from datetime import datetime
from typing import List


class Account:
    def __init__(self, initial_capital: float, current_balance: float, current_equity: float, last_update: str,
                 margin_used: float, max_floating_loss: float, max_floating_profit: float, max_profit: float,
                 max_loss: float, max_holding_bars: int):
        self.initial_capital = initial_capital
        self.current_balance = current_balance
        self.current_equity = current_equity
        self.last_update = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
        self.margin_used = margin_used
        self.max_floating_loss = max_floating_loss
        self.max_floating_profit = max_floating_profit
        self.max_profit = max_profit
        self.max_loss = max_loss
        self.max_holding_bars = max_holding_bars
