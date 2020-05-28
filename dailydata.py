import pandas as pd


# method for calculating day-based data
def dailypreps():
    data = pd.read_csv('data/chargers/Allschwile_1.csv')
    print(pd.head(data))


dailypreps()
