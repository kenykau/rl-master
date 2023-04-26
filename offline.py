import numpy as np
import pandas as pd
import mplfinance as mpf

df = pd.read_csv('HSI.csv', index_col='Date', parse_dates=True, na_values={
    'Open': 'null', 'High': 'null', 'Low': 'null', 'Close': 'null', 'Adj Close': 'null', 'Volume': 'null'})
df.dropna(how='all', subset=['Open', 'High', 'Low',
          'Close', 'Adj Close', 'Volume'], inplace=True)

# assuming your dataframe is already read into a variable named 'df'
df['fractal'] = 0   # set the default value of fractal to 0

for i in range(2, len(df)-2):
    if df['High'][i] == max(df['High'][i-2:i+3]) and df['High'][i] != df['High'][i-1] and df['High'][i] != df['High'][i-2] and df['High'][i] != df['High'][i+1] and df['High'][i] != df['High'][i+2]:
        df['fractal'][i] = 1
    elif df['Low'][i] == min(df['Low'][i-2:i+3]) and df['Low'][i] != df['Low'][i-1] and df['Low'][i] != df['Low'][i-2] and df['Low'][i] != df['Low'][i+1] and df['Low'][i] != df['Low'][i+2]:
        df['fractal'][i] = -1

upperFractals = df[df['fractal'] == 1]
lowerFractals = df[df['fractal'] == -1]

# compute the trendline slope and deviation


def compute(df, fractal, pattern, n, idx):
    # Get the relevant fractal data from either `upperFractal` or `lowerFractal`
    if pattern == 1:
        fractal_data = fractal.iloc[idx:idx+n]
    elif pattern == -1:
        fractal_data = fractal.iloc[idx:idx+n]
    else:
        raise ValueError("Invalid pattern value. Must be 1 or -1.")

    dates = list(fractal_data.index)
    df_range = df.loc[(df.index >= dates[0]) &
                      (df.index <= dates[-1])]
    extreme = 'High' if pattern == 1 else 'Low'
    data_len = len(df_range)
    pt0 = fractal_data.loc[dates[0], extreme]
    pt1 = fractal_data.loc[dates[-1], extreme]
    slope = (pt1 - pt0)/data_len
    std_dev = df_range[extreme].std()
    # print(data_len, pt0, pt1, slope, std_dev)
    return data_len, slope, std_dev


def checkFractals(df, fractals, idx):
    # get the index of df row
    df_idx = df.index[idx]

    # get the index of fractals for the df row
    fractal_idx = fractals.index.get_indexer([df_idx], method='ffill')[0]

    # if no match found, get the last row of fractal which date is less than the selected df date
    if fractals.index[fractal_idx] > df_idx:
        fractal_idx -= 1
    print(fractal_idx+1)
    # return how many rows in fractal df, which is date is less than or equal to the selected df date
    return fractal_idx + 1


compute(df, upperFractals, 1, 6, 0)
checkFractals(df, upperFractals, 20)
