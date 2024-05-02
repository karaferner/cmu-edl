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

def add_hours_column(df):
    df['hours'] = df['seconds']/3600
    return df

def combine_dataframes(dfs_list):
    combined_df = pd.concat(dfs_list)
    return combined_df

def sort_dataframe_by_time(df):
    df_sorted = df.sort_values(by="time/s")
    return df_sorted

def average_data_on_cycle_number(data_to_average=pd.DataFrame, num_rows_to_average=10):
    averaged_data = pd.DataFrame(columns=data_to_average.columns)
    grouped_data = data_to_average.groupby("cycle number")

    for cycle_num, group in grouped_data:
        sorted_group = group.sort_index(ascending=True)
        last_ten = sorted_group.tail(num_rows_to_average)
        for original_col_name in data_to_average.columns:
            if original_col_name == "time/s":
                time = pd.to_datetime(last_ten['time/s'])
                averaged_data.loc[cycle_num,original_col_name] = max(time)
            else:
                averaged_data.loc[cycle_num,original_col_name] = last_ten[original_col_name].mean()

    return averaged_data
    
def shift_indices(df, number_to_shift):
    df.index = df.index + number_to_shift
    return df

def skip_row_index(df, row_to_skip):
    new_index = df.index.to_series()
    new_index.loc[row_to_skip:] += 1
    df.index = new_index
    return df