import numpy as np
import csv
import io
import pandas as pd
import altair as alt


def get_data(filename):
    """
    Reads file into DataFrame.

    Parameters:
        filename (str): A string for the filename.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the files.
    """
    return pd.read_csv(filename, sep="\s+")


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


def get_pol_curve_data(high_current_data, low_current_data=None, convert_to_Amps=True):
    """
    Gets full polarization curve data, for time, voltage, and current. 

    Parameters:
        high_current_data (pd.DataFrame): A DataFrame containing the data for the high current regime.
        low_current_data (pd.DataFrame): A DataFrame containing the data for the low current regime.
        convert_to_Amps (Boolean): True if current should be converted from mA to A. Default value is True.

    Returns:
        pol_curve_data: A DataFrame containing the polarization curve data for time, voltage, and current. 
    """
    high_current_data = average_data_on_Ns(high_current_data)
   
    if low_current_data is not None:
        low_current_data = average_data_on_Ns(low_current_data)
        frames = [low_current_data, high_current_data]
        pol_curve_data = pd.concat(frames, ignore_index=True)
    else:
        pol_curve_data = high_current_data

    if convert_to_Amps:
        pol_curve_data["I/A"] = pol_curve_data["I/mA"]/1000
        
    pol_curve_data = pol_curve_data.drop(columns='Ns')

    return pol_curve_data

def plot_geom_area_norm_pol_curve(pol_curve_data, active_area=5):
    """
    Plots polarization curve for geometric area normlized current density.

    Parameters:
        pol_curve_data (pd.DataFrame): A DataFrame containing the polarization curve data for time, voltage, and current.
        active_area (float): A float for the cell's geometric active area, in cm^2. Default value is 5 cm^2. 

    Returns:
        pol_curve_data: A DataFrame containing the polarization curve data for time, voltage, and current. 
    """

    pol_curve_data["I/A cm-2"] = pol_curve_data["I/A"]/active_area

    chart = alt.Chart(pol_curve_data).mark_point().encode(
        alt.X('I/A cm-2',scale=alt.Scale(domain=[0,3])),
        alt.Y('<Ewe>/V',scale=alt.Scale(domain=[1.38,2.1]))
    )

    chart.save('chart.HTML')

if __name__ == "__main__":
    print('hello world')
    df_high_current = get_data("test_data/test_data_highIVcurve.txt")
    df_low_current = get_data("test_data/test_data_lowIVcurve.txt")
    pol_curve_data_test = get_pol_curve_data(df_high_current, low_current_data=df_low_current)
    plot_geom_area_norm_pol_curve(pol_curve_data_test)