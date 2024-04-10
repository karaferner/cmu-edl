import csv
import numpy as np
from datetime import datetime
import os
import re
import pandas as pd

def readCSVdata(filename):
    dataframe = pd.read_csv(filename,sep='\s+')
    return dataframe


# def writeCSV(data):
#     with open('output.csv', 'w',newline='') as csvfile:
#         csvwriter = csv.writer(csvfile)
#         csvwriter.writerows(data)
#     print('output.csv written')


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

    print()
    return dataframe

def check_for_extra_commas(dataframe):
    num_columns = len(dataframe.columns)

    rows_to_delete = []
    for index, row in dataframe.iterrows():
        
        try:
            assert len(row) == num_columns
        except AssertionError:
            if len(row) == num_columns+1:
                print(f"AssertionError raised at row {index}, length of row: {len(row)}, extra comma")
                rows_to_delete.append(index)
    
    for j in reversed(rows_to_delete):
        del dataframe[j]

    print()
    return dataframe

def strip_column_names(dataframe):
    headers = dataframe.columns.values
    print(headers)
    for i,name in enumerate(headers):
        clean_name = name.replace("<", "").replace(">", "")
        dataframe.columns.values[i] = clean_name
    return dataframe


def clean_data_file(filename):
    data = readCSVdata(filename)
    data = check_for_missing_newline(data)
    data = check_for_extra_commas(data)
    data = strip_column_names(data)
    return data

if __name__ == "__main__":
    filename = 'test_data/test_data_highIVcurve.txt'
    data = readCSVdata(filename)

    writeCSV(data)
    