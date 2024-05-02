import numpy as np
import pandas as pd
import altair as alt
from data_cleaning import read_and_clean_data
from useful_funcs import *

class Durability:
    def __init__(self,experiment):
        self.experiment = experiment

    def getTimeData_Cycling(filenames):
        dfs_list = []
        for file in filenames:
            df = pd.read_csv(file, sep="\t(?!\t$)", engine='python')
            dfs_list.append(df)
        
        combined_df = combine_dataframes(dfs_list)
        time_sorted_df = sort_dataframe_by_time(combined_df)
        rel_time_df = convert_abs_time_to_total_seconds(time_sorted_df)
        
        return rel_time_df