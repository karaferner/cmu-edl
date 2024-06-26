import numpy as np
import pandas as pd
import altair as alt
from data_cleaning import read_and_clean_data

class CyclicVoltammetry:
    def __init__(self,experiment):
        self.CV_data = None

        self.experiment = experiment

    def add_CV_data(self, CV_data_file):
        self.CV_data = read_and_clean_data(CV_data_file)

    def get_CV_data(self):
        return self.CV_data
    
    def select_cycle(self, cycle_number=10):
        self.CV_data = self.CV_data[self.CV_data['cycle number'] == cycle_number]
        return self.CV_data
    
    def plot_CV(self):
        CV_plot = alt.Chart(self.CV_data).mark_circle().encode(
            alt.X("Ewe/V"),
            alt.Y("I/mA")
            ).interactive()
        
        CV_plot.save('test_output/CV_plot.html')