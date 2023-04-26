from datetime import datetime


class IndicatorData:
    def __init__(self, fractals: int, dt1: str, dt2: str, v1: float, v2: float, slope: float, std_dev: float, bars: int,
                 current_value: float, current_std_value: float, fractal_type: str):
        self.fractals = fractals
        self.dt1 = datetime.strptime(dt1, '%Y-%m-%d %H:%M:%S')
        self.dt2 = datetime.strptime(dt2, '%Y-%m-%d %H:%M:%S')
        self.v1 = v1
        self.v2 = v2
        self.slope = slope
        self.std_dev = std_dev
        self.bars = bars
        self.current_value = current_value
        self.current_std_value = current_std_value
        self.fractal_type = fractal_type
