import numpy as np
import csv
import io
import pandas as pd
import altair as alt

class Polarization:
    def __init__(self,experiment):
        self.high_current_data = None
        self.low_current_data = None

        self.experiment = experiment
    
    def add_high_current_data(self, data_file):
        self.high_current_data = pd.read_csv(data_file, sep="\s+")

    def add_low_current_data(self, data_file):
        self.low_current_data = pd.read_csv(data_file,sep='\s+')

    def get_high_current_data(self):
        return self.high_current_data
    
    def get_low_current_data(self):
        return self.low_current_data

    def average_data_on_Ns(df=pd.DataFrame, num_rows=10):
        """
        Calculates the average of the last rows of data for each value "Ns".

        Parameters:
            df (pd.DataFrame): A DataFrame containing the data.
            num_rows (int): The number of rows (data points) to average for each "Ns." Default value is 10. 

        Returns:
            df_avg: A DataFrame containing the averaged data
        """

        df_avg = pd.DataFrame(columns=df.columns)
        grouped = df.groupby("Ns")

        for name, group in grouped:
            sorted_group = group.sort_index(ascending=True)
            last_ten = sorted_group.tail(num_rows)
            for col in df.columns:
                df_avg.loc[name,col] = last_ten[col].mean()

        return df_avg


    def get_pol_curve_data(self, convert_to_Amps=True):
        """
        Gets full polarization curve data, for time, voltage, and current. 

        Parameters:
            filename_high_current_data (string): A string containing the path to file for the high current data.
            filename_low_current_data (string): A string containing the path to file for the low current data.
            convert_to_Amps (Boolean): True if current should be converted from mA to A. Default value is True.

        Returns:
            pol_curve_data: A DataFrame containing the polarization curve data for time, voltage, and current. 
        """
        

        self.high_current_data = Polarization.average_data_on_Ns(self.high_current_data)
    
        if self.add_low_current_data is not None:
            self.low_current_data = Polarization.average_data_on_Ns(self.low_current_data)
            frames = [self.low_current_data, self.high_current_data]
            self.pol_curve_data = pd.concat(frames, ignore_index=True)
        else:
            self.pol_curve_data = self.high_current_data

        if convert_to_Amps:
            self.pol_curve_data["I/A"] = self.pol_curve_data["I/mA"]/1000
            
        self.pol_curve_data = self.pol_curve_data.drop(columns='Ns')

        return self.pol_curve_data

    def normalize_current_to_geom_area(self):
        """
        Plots polarization curve for geometric area normlized current density.

        Parameters:
            pol_curve_data (pd.DataFrame): A DataFrame containing the polarization curve data for time, voltage, and current.
            active_area (float): A float for the cell's geometric active area, in cm^2. Default value is 5 cm^2. 

        Returns:
            pol_curve_data: A DataFrame containing the polarization curve data for time, voltage, and current. 
        """

        self.pol_curve_data["I/A cm^-2"] = self.pol_curve_data["I/A"]/self.experiment.active_area
        return self.pol_curve_data

    def normalize_current_to_Ir_loading(self):
        self.pol_curve_data["I/A mg_Ir^-1"] = self.pol_curve_data["I/A cm^-2"]/self.experiment.Ir_loading
        return self.pol_curve_data

    def normalize_current_to_catalyst_cost(self, Ir_price=5000, Pt_price=1000):
        Ir_price = Ir_price/  28349.523125 #$/oz / mg/oz = $/mg
        Pt_price = Pt_price / 28349.523125 #$/oz / mg/oz = $/mg

        Ir_part = self.experiment.Ir_loading*Ir_price
        Pt_part = self.experiment.Pt_loading*Pt_price
        total_cost = Ir_part+Pt_part #total $/cm^2
        self.pol_curve_data["I/A $PGM^-1"] = self.pol_curve_data["I/A cm^-2"]/total_cost
        return self.pol_curve_data

    # def plot_pol_curves(pol_curve_data, geom_area=True, Ir_loading=False, cost=False):
    #     if geom_area:
    #         pol_curve_data = normalize_current_to_geom_area(pol_curve_data)

    #         geom_area_norm_pol_curve = alt.Chart(pol_curve_data).mark_circle().encode(
    #         alt.X('I/A cm^-2', axis=alt.Axis(title='Current density [A cm-2]')),
    #         alt.Y('<Ewe>/V',axis=alt.Axis(title='Cell voltage [V]'),scale=alt.Scale(domain=[1.38,2.4]))
    #         )

    #     if Ir_loading:
    #         pol_curve_data = normalize_current_to_Ir_loading(pol_curve_data, Ir_loading=0.1)

    #         Ir_loading_norm_pol_curve = alt.Chart(pol_curve_data).mark_circle().encode(
    #         alt.X('I/A mg_Ir^-1', axis=alt.Axis(title='Current density [A mg_Ir^-1]')),
    #         alt.Y('<Ewe>/V',axis=alt.Axis(title='Cell voltage [V]'),scale=alt.Scale(domain=[1.38,2.4]))
    #         )

    #     if cost:
    #         pol_curve_data = normalize_current_to_catalyst_cost(pol_curve_data)

    #         catalyst_cost_norm_pol_curve = alt.Chart(pol_curve_data).mark_circle().encode(
    #         alt.X('I/A $PGM^-1', axis=alt.Axis(title='Current density [A $PGM^-1]')),
    #         alt.Y('<Ewe>/V',axis=alt.Axis(title='Cell voltage [V]'),scale=alt.Scale(domain=[1.38,2.4]))
    #         )

    #     composite_chart = geom_area_norm_pol_curve | Ir_loading_norm_pol_curve
    
    #     composite_chart.save('pol_curves.html')

        