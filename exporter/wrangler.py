import pandas as pd
import numpy as np
import re

def seperate_songname(string):
    split = string.split('-')
    if len(split) == 2:
        return re.sub('[^A-Za-z0-9]+', '', split[1].lower())
    else:
        return re.sub('[^A-Za-z0-9]+', '', split[0].lower())

if __name__ == "__main__":
    df = pd.read_csv('data/data.csv')
    
    df["name"] = df["name"].apply(lambda row: row.split('|')[0])
    df["artist"] = df["name"].apply(lambda row: re.sub('[^A-Za-z0-9]+', '', row.split('-')[0].lower()))
    df["song"] = df["name"].apply(lambda row: seperate_songname(row))

    df.to_csv('data/wrangled.csv')