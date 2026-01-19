import pandas as pd

def moving_average_forecast(series, window=7):
    return series.rolling(window).mean()
