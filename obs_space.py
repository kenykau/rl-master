from datetime import datetime
from typing import List
from account import Account
from position import Position
from indicator import Indicator


class ObservationSpace:
    def __init__(self, indicator_datas: List[Indicator], current_positions: List[Position], closed_positions: List[Position],
                 account_details: Account):
        self.account_details = account_details
        self.indicator_datas = indicator_datas
        self.current_positions = current_positions
        self.closed_positions = closed_positions
