import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

import taipy as tp
from taipy import Gui

months =['January', 'February', 'March', 'April', 'May', 'June', 
         'July', 'August', 'September', 'October', 'November', 'December']

months_abr = ['Jan-2022', 'Feb-2022', 'Mar-2022', 'Apr-2022', 'May-2022', 'Jun-2022', 'Jul-2022', 'Aug-2022', 'Sep-2022', 'Oct-2022', 'Nov-2022', 'Dec-2022']

df = pd.read_csv('data_daily.csv')
df['# Date'] = pd.to_datetime(df['# Date'])
X = np.arange(1, 366)
Y = df['Receipt_Count'].to_numpy()

prediction = None
month = ""

def calc_params(X,Y):
    """
    input: two numpy arrays of same length
    output: a list of coefficients of the line of best fit
    """
    denominator = X.dot(X) - X.mean() * X.sum()
    slope = (X.dot(Y) - Y.mean()* X.sum()) / denominator
    intercept = (Y.mean() * X.dot(X) - X.mean() * X.dot(Y)) / denominator

    return [slope, intercept]

def compute_date(name_of_month):
    """
    input: string containing the name of the month
    output: datetime date of the 15th of that month of 2022"""
    for idx, item in enumerate(months):
        if item == name_of_month:
            date = datetime.date(2022, idx + 1, 15)

    return date

def delta(name_of_month):
    """
    input: name of the month (string)
    output: number of days to the 15th of that month (int)"""
    date = compute_date(name_of_month)
    return (date - datetime.date(2021, 12,31)).days  


def get_monthly_prediction(name_of_month):
    """
    input: name of the month (str)
    output: predicted number of receipts for that month (int)"""
    m, b = calc_params(X,Y)
    incr = delta(name_of_month)
    pred = m * (365 + incr) + b

    return pred

def on_change_month(state):
    """
    this function updates the month and the prediction upon selection of the month"""
    month = state.month
    state.prediction = round(get_monthly_prediction(month)/1000000, 2)

def get_all_predictions():
    """
    output: the list of predictions for all months in 2022"""
    preds = []
    for i in months:
        pred = get_monthly_prediction(i)
        preds.append(pred)

    return preds

# data for the bar plot
predictions = get_all_predictions()
d = {'Months': months_abr, 'Predictions': predictions}
predictions_df = pd.DataFrame(data=d)




page = """

<center> <h1> Receipt Count Prediction </h1> </center>


<|layout| columns=1 1|
  <|{month}|selector|lov={months}|on_change=on_change_month|dropdown|label=Month|>
  <|part| class_name=container|
   Predicted number of receipts in million:
  <|{prediction}|text|raw|> 
  |>
|>
<br/>
<br/>
<|part|class_name=container|
  <|{predictions_df}|chart|type=bar|x=Months|y=Predictions|title=Predicted receipt count |>
|>

"""

if __name__ == '__main__':
    
    Gui(page=page).run()