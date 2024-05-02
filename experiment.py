import numpy as np
import csv
import io
import pandas as pd
import altair as alt
from polarization import Polarization
from EIS import EIS
from cyclic_voltammetry import CyclicVoltammetry
from durability import Durability


class Experiment:
    def __init__(self, name, iridium_loading=None, platinum_loading=None, active_area=None):
        self.name = name
        self.iridium_loading = iridium_loading
        self.platinum_loading = platinum_loading
        self.active_area = active_area
        self.polarization = Polarization(self)
        self.EIS = EIS(self)
        self.CV = CyclicVoltammetry(self)
        self.durability = Durability(self)
    
    def print_details(self):
        print("Experiment Details:")
        print("Experiment Name:", self.name)
        print("Ir Loading:", self.iridium_loading)
        print("Pt Loading:", self.platinum_loading)
        print("Active Area: {} cm^2".format(self.active_area))

    def set_Ir_loading(self, iridium_loading):
        self.iridium_loading = iridium_loading

    def get_Ir_loading(self):
        return self.iridium_loading

    def set_Pt_loading(self, platinum_loading):
        self.platinum_loading = platinum_loading

    def get_Pt_loading(self):
        return self.platinum_loading

    def set_active_area(self, active_area):
        self.active_area = active_area

    def get_active_area(self):
        return self.active_area