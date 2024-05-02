import numpy as np

def calc_HFR(df):
    real = np.array(df['Re(Z)/Ohm'])
    im = np.array(df['-Im(Z)/Ohm'])
    
    for j in range(len(im)):
        if im[j]<0 and im[j+1]>0:
            HFR = ((real[j+1]+real[j])/2)
            break
            
    return HFR


def get_HFR_array(df):
    grouped = df.groupby("cycle number")
    HFR_list_for_given_df = []
    for cycle_num, group in grouped:
        HFR = calc_HFR(group)
        HFR_list_for_given_df.append(HFR)
            
    return np.array(HFR_list_for_given_df)


def calc_HFR_free(df):
    average_HFR = np.average(df['HFR'])
    print(average_HFR)
    df['EiR-Free/V'] = df['Ewe/V'] - ((df['I/mA']/1000)*average_HFR)
    return df