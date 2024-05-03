import numpy as np
import pandas as pd
import altair as alt
from data_cleaning import read_and_clean_data
from useful_funcs import *
from analysis.HFR import *

class Durability:
    def __init__(self,experiment):
        self.experiment = experiment
        self.cycling = None
        self.PEIS = None
        self.per_hour_current_hold = None
        self.per_hour_GEIS = None

    def add_cycling_data(self, directory):
        filenames = get_filenames(directory)
        dfs_list = []
        for file in filenames:
            df = read_and_clean_data(file)
            dfs_list.append(df)
        
        combined_df = combine_dataframes(dfs_list)
        time_sorted_df = sort_dataframe_by_time(combined_df)
        rel_time_df = convert_abs_time_to_total_seconds(time_sorted_df)
        rel_time_df = add_hours_column(rel_time_df)
        
        self.cycling =  rel_time_df

    def get_cycling_data(self):
        return self.cycling
    
    def add_per_hour_data(self, directory):
        filenames = get_filenames(directory)
        current_hold_list = []
        GEIS_list = []

        for file in filenames:
            df = read_and_clean_data(file)

            current_hold = df[df['freq/Hz']== 0]
            current_hold = current_hold.drop(columns=['freq/Hz','Re(Z)/Ohm','-Im(Z)/Ohm'])
            current_hold = current_hold[current_hold['cycle number']== 1]
            current_hold = average_data_on_cycle_number(current_hold)
            current_hold_list.append(current_hold)

            GEIS = df[df['freq/Hz']!= 0]
            GEIS = GEIS[GEIS['cycle number']== 1]
            HFRs = get_HFR_array(GEIS)
            GEIS = average_data_on_cycle_number(GEIS)
            GEIS['HFR'] = HFRs
            GEIS_list.append(df)
                
        current_hold_df = combine_dataframes(current_hold_list)
        current_hold_df = sort_dataframe_by_time(current_hold_df)
        current_hold_df = convert_abs_time_to_total_seconds(current_hold_df)
        current_hold_df = current_hold_df.reset_index(drop=True)
        
        GEIS_df = combine_dataframes(GEIS_list)
        GEIS_df = sort_dataframe_by_time(GEIS_df)
        GEIS_df = GEIS_df.reset_index(drop=True)

        self.per_hour_current_hold = current_hold_df
        self.per_hour_GEIS = GEIS_df


    def getPolCurve_SGEIS(filenames):
        dfs_list = []
        for file in filenames:
            df = pd.read_csv(file, sep=r"\t", engine='python')
            df = df[df['freq/Hz']== 0]
            df = df.drop(columns=['freq/Hz','Re(Z)/Ohm','-Im(Z)/Ohm'])
            df = average_data_on_cycle_number(df)
            dfs_list.append(df)
            
        combined_df = combine_dataframes(dfs_list)
        time_sorted_df = sort_dataframe_by_time(combined_df)
        df_reset = time_sorted_df.reset_index(drop=True)
        
        return df_reset
