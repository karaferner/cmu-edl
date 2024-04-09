import numpy as np
import csv
import io
import pandas as pd
import altair as alt
from polarization import Polarization

class Experiment:
    def __init__(self, name, Ir_loading, Pt_loading, active_area):
        self.name = name
        self.iridium_loading = Ir_loading
        self.platinum_loading = Pt_loading
        self.active_area = active_area
        self.polarization = Polarization()
    
    def print_details(self):
        print("Experiment Details:")
        print("Experiment Name:", self.name)
        print("Ir Loading:", self.iridium_loading)
        print("Pt Loading:", self.platinum_loading)
        print("Active Area:", self.active_area)