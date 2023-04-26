class ticker:
    def __init__(self, tick: str, margin_required_per_lot: float, margin_maintained_per_lot: float, digits: int):
        self.tick = tick
        self.margin_required_per_lot = margin_required_per_lot
        self.margin_maintained_per_lot = margin_maintained_per_lot
        self.digits = digits
