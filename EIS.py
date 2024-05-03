import numpy as np
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

    def add_EIS_data(self, EIS_data_file):
        self.EIS_data = read_and_clean_data(EIS_data_file)
        self.real_impedance = self.EIS_data.loc[:,"Re(Z)/Ohm"]
        self.imaginary_impedance = self.EIS_data.loc[:,"-Im(Z)/Ohm"]

    def get_EIS_data(self):
        return self.EIS_data
    
    def calc_HFR(self):
        real = np.array(self.EIS_data['Re(Z)/Ohm'])
        im = np.array(self.EIS_data['-Im(Z)/Ohm'])
        
        for j in range(len(im)):
            if im[j]<0 and im[j+1]>0:
                HFR = ((real[j+1]+real[j])/2)
                break
                
        return HFR
    
    def plot_Nyquist(self):

        Nyquist_plot = alt.Chart(self.EIS_data).mark_circle().encode(
            alt.X("Re(Z)/Ohm"),
            alt.Y("-Im(Z)/Ohm")
            ).interactive()
        
        Nyquist_plot.save('test_output/EIS_Nyquist.html')