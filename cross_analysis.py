import numpy as np
# from scipy.interpolate import interp1d


def tafel(x,b,i0):
    y = []
    for i in x:
        y.append(b*np.log10(i/(i0))+1.182)
    return np.array(y)


# def interpolate_activity(target,i,v):
#     interp_func = interp1d(v, i, kind='linear')
#     x_approx = interp_func(target)
#     print(f"Approximate i value at E_ir-free={target} V: {x_approx}")
#     return x_approx


def calc_HFR_free(df):
    average_HFR = np.average(df['HFR'])
    print(average_HFR)
    df['EiR-Free/V'] = df['<Ewe>/V'] - ((df['<I>/mA']/1000)*average_HFR)
    return df