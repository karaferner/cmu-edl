import numpy as np
import csv
import io
import pandas as pd
import altair as alt
from polarization import Polarization

class Experiment:
    def __init__(self, name, Ir_loading, Pt_loading, active_area):
        self.name = name
        self.Ir_loading = Ir_loading
        self.Pt_loading = Pt_loading
        self.active_area = active_area
        self.polarization = Polarization(self)
    
    def print_details(self):
        print("Experiment Details:")
        print("Experiment Name:", self.name)
        print("Ir Loading:", self.Ir_loading)
        print("Pt Loading:", self.Pt_loading)
        print("Active Area:", self.active_area)