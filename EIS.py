import numpy as np
import csv
import io
import pandas as pd
import altair as alt
from data_cleaning import read_and_clean_data

class EIS:
    def __init__(self,experiment):
        self.EIS_data = None
        self.real_impedance = None
        self.imaginary_impedance = None
        self.HFR = None

        self.experiment = experiment

    def add_EIS_data(self, data_file):
        self.EIS_data = read_and_clean_data(data_file)
        self.real_impedance = self.EIS_data.loc[:,"Re(Z)/Ohm"]
        self.imaginary_impedance = self.EIS_data.loc[:,"-Im(Z)/Ohm"]

    def get_EIS_data(self):
        return self.EIS_data
    
    def get_HFR(self):      
        for i, im in enumerate(self.imaginary_impedance):
            if im<0 and self.imaginary_impedance[i+1]>0:
                self.HFR = (self.real_impedance[i+1]+self.real_impedance[i])/2
                self.HFR *= self.experiment.active_area
                break
        return self.HFR
    
    def plot_Nyquist(self):

        Nyquist_plot = alt.Chart(self.EIS_data).mark_circle().encode(
            alt.X("Re(Z)/Ohm"),
            alt.Y("-Im(Z)/Ohm")
            ).interactive()
        
        Nyquist_plot.save('test_output/EIS_Nyquist.html')