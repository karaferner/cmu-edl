import csv
import numpy as np
from datetime import datetime
import os
import re
import pandas as pd

def read_txt_file(filename):
    dataframe = pd.read_csv(filename,sep=r'\t(?!\t$)', engine='python')
    return dataframe


def check_for_missing_newline(dataframe):
    num_columns = len(dataframe.columns)
    for index, row in dataframe.iterrows():
        try:
            assert len(row) == num_columns
        except AssertionError:
            if len(row) == 2*num_columns-1:
                print(f"AssertionError raised at row {index}, length of row: {len(row)}, missing newline")
                for j, value in enumerate(row):
                    if j == num_columns-1:
                        split_values = value.split('"')
 
                        replace_current_row = row[0:j] + [split_values[0]]
                        second_row = [split_values[1]] + row[j+1:]

                        dataframe[index] = replace_current_row
                        dataframe.insert(index+1,second_row)

    return dataframe

def check_for_extra_separator(dataframe):
    num_columns = len(dataframe.columns)

    rows_to_delete = []
    for index, row in dataframe.iterrows():
        
        try:
            assert len(row) == num_columns
        except AssertionError:
            if len(row) == num_columns+1:
                print(f"AssertionError raised at row {index}, length of row: {len(row)}, extra separator")
                rows_to_delete.append(index)
    
    for j in reversed(rows_to_delete):
        del dataframe[j]

    return dataframe

def strip_column_names(dataframe):
    headers = dataframe.columns.values
    for i,name in enumerate(headers):
        clean_name = name.replace("<", "").replace(">", "")
        dataframe.columns.values[i] = clean_name
    return dataframe


def read_and_clean_data(filename):
    data = read_txt_file(filename)
    data = check_for_missing_newline(data)
    data = check_for_extra_separator(data)
    data = strip_column_names(data)
    return data


    