import numpy as np
import csv
import io
import pandas as pd
import altair as alt

class CyclicVoltammetry:
    def __init__(self,experiment):
        self.CV_data = None

        self.experiment = experiment

    def add_CV_data(self, data_file):
        self.CV_data = pd.read_csv(data_file, sep="\s+")
        self.CV_data = self.CV_data.drop(columns='number')

    def get_CV_data(self):
        return self.CV_data
    
    def select_cycle(self, cycle_num=10):
        self.CV_data = self.CV_data[self.CV_data['cycle'] == cycle_num]
        return self.CV_data
    
    def plot_CV(self):
        CV_plot = alt.Chart(self.CV_data).mark_circle().encode(
            alt.X("Ewe/V"),
            alt.Y("<I>/mA")
            )
        
        CV_plot.save('CV_plot.html')