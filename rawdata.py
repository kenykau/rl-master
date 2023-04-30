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

def Compute(raw: pd.DataFrame, fractal: pd.DataFrame, n: int, idx: int):
    if idx <= 2:
        return None

    current_row = raw.iloc[idx]
    current_index = raw.index[idx - 2]

    # Find the closest Fractal index, but must be less than current_index
    last_fractal = fractal[fractal.index < current_index].iloc[-1]

    if last_fractal.empty:
        return None

    # Get n rows of data from Fractal
    n_rows = fractal.loc[:last_fractal.name].iloc[-n:]

    # If the data is less than n rows, return None
    if len(n_rows) < n:
        return None

    # Create variables named row0 and row1
    row0 = raw.loc[n_rows.index[0]]
    row1 = raw.loc[n_rows.index[-1]]

    # Calculate the number of rows between row0 and row1 (including row0 and row1)
    n_bars = len(raw.loc[row0.name:row1.name])

    # Store all rows between row0 and row1 (including row0 and row1)
    bars = raw.loc[row0.name:row1.name]

    # Call the Calculate function and store the returned values in variables
    slope, intercept, line, std_dev = Calculate(bars, 'High')

    # Calculate the position of current_row relative to bars DataFrame
    current_row_position = raw.index.get_loc(current_row.name) - raw.index.get_loc(bars.index[0])


    # Predict the value of current_row using the linear regression line
    predicted_value = slope * current_row_position + intercept

    # Add the line and std_dev variables to the return statement
    return n, last_fractal, row0, row1, n_bars, bars, predicted_value



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

    return lr.coef_[0][0], lr.intercept_[0], line, std_dev

def prepare_data(data_folder: str, file_name: str):
    project_path = os.getcwd()
    file_path = os.path.join(project_path, data_folder, file_name)

    dataframe = read_csv_to_dataframe(file_path)
    dataframe = calculate_fractal(dataframe)

    fractal_df = dataframe[dataframe['Fractal'] != 0].copy()
    filtered_df_2 = fractal_df[fractal_df['Fractal'] == 2]

    upper_fractal_df = dataframe[dataframe['UpperFractal']].copy()
    lower_fractal_df = dataframe[dataframe['LowerFractal']].copy()

    print(upper_fractal_df.head(10))
    print(dataframe.head(100))
    Compute(dataframe, upper_fractal_df, 3, 26)


if __name__ == '__main__':
    data_folder = 'data'
    file_name = 'USA30IDXUSD.csv'
    prepare_data(data_folder, file_name)