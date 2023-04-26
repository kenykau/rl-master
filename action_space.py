class ActionSpace:
    def __init__(self, action_type: str, lots: int, stop_loss: float, take_profit: float):
        self.type = action_type
        self.lots = lots
        self.stop_loss = stop_loss
        self.take_profit = take_profit
