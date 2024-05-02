import numpy as np
import csv
import io
import pandas as pd
import altair as alt
import matplotlib as plt
import os

def get_filenames(directory):
    filenames = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path) and full_path.endswith(".txt"):
            filenames.append(full_path)
        elif os.path.isdir(full_path):
            filenames.extend(get_filenames(full_path))
    return filenames


def convert_abs_time_to_total_seconds(df):
    df['seconds'] = pd.to_datetime(df['time/s'])
    df['seconds'] = (df['seconds'] - df['seconds'].min()).dt.total_seconds() + 0.1
    return df

def combine_dataframes(dfs_list):
    combined_df = pd.concat(dfs_list)
    return combined_df

def sort_dataframe_by_time(df):
    df_sorted = df.sort_values(by="time/s")
 
    return df_sorted
    