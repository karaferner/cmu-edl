import numpy as np
import csv
import io
import pandas as pd


def get_data(filename):
    return pd.read_csv(filename, sep="\s+")


def get_pol_curve(data):
    grouped = data.groupby("Ns")
    results = pd.DataFrame(columns=["voltage_avg", "current_avg"])
    
    for name, group in grouped:
        sorted_group = group.sort_index(ascending=True)
        last_ten = group.tail(10)

        voltage_avg = last_ten["<Ewe>/V"].mean()
        current_avg = last_ten["I/mA"].mean()/(5*1000)
        new_row = pd.DataFrame([{"voltage_avg": voltage_avg, "current_avg": current_avg}])

        results = pd.concat([results,new_row],ignore_index=True )
    return results











    