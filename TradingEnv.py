import gym


class TradingEvn(gym.Env):
    def __init__(self, df, window_size, frame_bound_list):
        self.df = df
        self.window_size = window_size
