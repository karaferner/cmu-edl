import numpy as np
import csv
import io
import pandas as pd
import altair as alt
from polarization import Polarization
from EIS import EIS
from cyclic_voltammetry import CyclicVoltammetry


class Experiment:
    def __init__(self, name, Ir_loading=None, Pt_loading=None, active_area=None):
        self.name = name
        self.Ir_loading = Ir_loading
        self.Pt_loading = Pt_loading
        self.active_area = active_area
        self.polarization = Polarization(self)
        self.EIS = EIS(self)
        self.CV = CyclicVoltammetry(self)
    
    def print_details(self):
        print("Experiment Details:")
        print("Experiment Name:", self.name)
        print("Ir Loading:", self.Ir_loading)
        print("Pt Loading:", self.Pt_loading)
        print("Active Area: {} cm^2".format(self.active_area))

    def set_Ir_loading(self, Ir_loading):
        self.Ir_loading = Ir_loading

    def get_Ir_loading(self):
        return self.Ir_loading

    def set_Pt_loading(self, Pt_loading):
        self.Pt_loading = Pt_loading

    def get_Pt_loading(self):
        return self.Pt_loading

    def set_active_area(self, active_area):
        self.active_area = active_area

    def get_active_area(self):
        return self.active_area