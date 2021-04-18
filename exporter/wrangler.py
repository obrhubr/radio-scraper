import pandas as pd
import numpy as np
import re

def seperate_songname(string):
    split = string.split('-')
    if len(split) == 2:
        return split[1]
    else:
        return split[0]

if __name__ == "__main__":
    df = pd.read_csv('data/data.csv', index_col=0)
    
    df["name"] = df["name"].apply(lambda row: row.split('|')[0])
    df["artist"] = df["name"].apply(lambda row: row.split('-')[0])
    df["song"] = df["name"].apply(lambda row: seperate_songname(row))

    df.to_csv('data/wrangled.csv')