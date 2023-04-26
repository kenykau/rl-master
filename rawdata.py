import pandas as pd
from typing import List
from datetime import datetime
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def read_csv_to_dataframe(file_path: str) -> pd.DataFrame:
    column_names = ['Date', 'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.read_csv(file_path, header=0, names=column_names)
    df['DT'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Timestamp'])
    df.set_index('DT', inplace=True)
    df.drop(['Date', 'Timestamp'], axis=1, inplace=True)
    return df

def calculate_fractal(df: pd.DataFrame) -> pd.DataFrame:
    df['UpperFractal'] = (
        (df['High'] > df['High'].shift(-1)) &
        (df['High'] > df['High'].shift(-2)) &
        (df['High'] > df['High'].shift(1)) &
        (df['High'] > df['High'].shift(2))
    )

    df['LowerFractal'] = (
        (df['Low'] < df['Low'].shift(-1)) &
        (df['Low'] < df['Low'].shift(-2)) &
        (df['Low'] < df['Low'].shift(1)) &
        (df['Low'] < df['Low'].shift(2))
    )

    df['Fractal'] = 0
    df.loc[(df['UpperFractal'] == True) & (df['LowerFractal'] == False), 'Fractal'] = 1
    df.loc[(df['UpperFractal'] == False) & (df['LowerFractal'] == True), 'Fractal'] = -1
    df.loc[(df['UpperFractal'] == True) & (df['LowerFractal'] == True), 'Fractal'] = 2

    return df



# Get the current working directory (project path)
project_path = os.getcwd()

# Join the project path, data folder, and CSV file name
file_name = 'USA30IDXUSD.csv'
data_folder = 'data'
file_path = os.path.join(project_path, data_folder, file_name)

# Read the CSV file and create a DataFrame
dataframe = read_csv_to_dataframe(file_path)
dataframe = calculate_fractal(dataframe)

fractal_df = dataframe[dataframe['Fractal']!=0].copy()

filtered_df_2 = fractal_df[fractal_df['Fractal'] == 2]

upper_fractal_df = dataframe[dataframe['UpperFractal']].copy()
lower_fractal_df = dataframe[dataframe['LowerFractal']].copy()
import pandas as pd

import pandas as pd

import pandas as pd

def Compute(raw: pd.DataFrame, fractal: pd.DataFrame, n: int, idx: int):
    if idx <= 2:
        return None

    current_row = raw.iloc[idx]
    current_index = raw.index[idx - 2]

    # 找到最接近的Fractal索引，但必须小于current_index
    last_fractal = fractal[fractal.index < current_index].iloc[-1]

    if last_fractal.empty:
        return None

    # 从Fractal中获取n行数据
    n_rows = fractal.loc[:last_fractal.name].iloc[-n:]

    # 如果数据不足n行，返回None
    if len(n_rows) < n:
        return None

    # 创建名为row0和row1的变量
    row0 = raw.loc[n_rows.index[0]]
    row1 = raw.loc[n_rows.index[-1]]

    # 计算row0和row1之间的行数（包括row0和row1）
    n_bars = len(raw.loc[row0.name:row1.name])

    # 存储row0和row1之间的所有行（包括row0和row1）
    bars = raw.loc[row0.name:row1.name]

    Calculate(bars, 'High')

    return n, last_fractal, row0, row1, n_bars, bars


def Calculate(bars: pd.DataFrame, appliedPrice: str):
    if appliedPrice == "High":
        data = bars['High']
    elif appliedPrice == "Low":
        data = bars['Low']
    elif appliedPrice == "Close":
        data = bars['Close']
    else:
        raise ValueError("Invalid appliedPrice. Must be 'High', 'Low', or 'Close'")

    # Compute linear regression line
    X = np.arange(len(data)).reshape(-1, 1)
    y = data.values.reshape(-1, 1)
    lr = LinearRegression()
    lr.fit(X, y)
    line = lr.predict(X)

    # Compute standard deviation
    std_dev = np.std(data)

    return line, std_dev


print(upper_fractal_df.head(10))
print(dataframe.head(100))
Compute(dataframe, upper_fractal_df, 3, 26)