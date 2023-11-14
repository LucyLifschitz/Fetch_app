import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

months =['january', 'february', 'march', 'april', 'may', 'june', 
         'july', 'august', 'september', 'october', 'november', 'december']

months_abr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def calc_params(X,Y):
    """
    input: two numpy arrays of same length
    output: a list of coefficients of the line of best fit
    """
    denominator = X.dot(X) - X.mean() * X.sum()
    slope = (X.dot(Y) - Y.mean()* X.sum()) / denominator
    intercept = (Y.mean() * X.dot(X) - X.mean() * X.dot(Y)) / denominator

    return [slope, intercept]

def my_line(x, slope, intercept):
    """input: value x, slope, intercept
      output: value of a linear function with these slope and intercept at x"""
    return slope * x + intercept

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

def predict_receipts(name_of_month, slope, intercept):
    """ 
    input: month (string), slope and intercept of the line of best fit
    output: predicted average of the number of receipts that month (int)
    We approximate predicted monthly average by the number of receipts on the 15th of that month"""
    increment = delta(name_of_month)
    pred = my_line(365+increment, slope, intercept)

    return pred

def get_ticks_labels():
    """function to generate ticks labels in the plot"""
    labels = []
    years = [2021, 2022]
    for i in years:
        for j in months_abr:
            date = j + '-' + str(i)
            labels.append(date)
    return labels

def get_ticks():
    """function to generate ticks for the plot"""
    ticks = []
    years = [2021, 2022]
    for i in years:
      for j in range(1,13):
        idx = (datetime.date(i, j, 15) - datetime.date(2020, 12,31)).days
        ticks.append(idx)

    return ticks

def plot_predictions(slope, intercept, x_range, name_of_month, pred): 
    """
    plots the line of best fit and the prediction for a given month"""
    x = np.array(x_range)
    y = slope * x + intercept 
    fig, ax = plt.subplots(figsize = (12, 6))
    plt.title('Predicted Receipt Count', fontsize=16)
    plt.ylabel('Count in tens of million')
    plt.xlabel('Month')
    plt.plot(x, y, color='red', linewidth=2) 
    plt.axhline(y = pred, color='black', linestyle = '--')
    plt.axvline(x = 365 + delta(name_of_month), color = 'black', linestyle = '--')
    ticks = get_ticks()
    labels = get_ticks_labels()
    plt.xticks(ticks=ticks, labels=labels, rotation=45)
    plt.text(5, predict_receipts(name_of_month, slope, intercept) + 1.e5, '%.2f million receipts' % (predict_receipts(name_of_month, slope, intercept)/1000000), fontsize=16 )
    plt.show()  



if __name__ == '__main__':
    # get data
    df = pd.read_csv('data_daily.csv')
    df['# Date'] = pd.to_datetime(df['# Date'])
    X = np.arange(1, 366)
    Y = df['Receipt_Count'].to_numpy()

    month = 'march'
    m, b = calc_params(X,Y)
    prediction = predict_receipts(month, m, b)
    incr = delta(month)
    plot_predictions(m, b, range(1, 731), month, prediction)

