"""
INFO

Functions to parse various flr, ECS data

Created by Joshua Temple
Assistance from Oliver Tessmer

Created 2018-03-27

@jtspree
"""

# LIBRARY

import pandas as pd
import os

# FUNCTION

# parse ECS DCMU P700 data
ECS_DIRK_DCMU_P700_suffix = "dcmu_p700_0005.dat"
def parse_ECS_DCMU_P700_data(folder):
    ECS_DCMU_P700_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(ECS_DIRK_DCMU_P700_suffix):
            ECS_DCMU_P700_filename = filename
    if (ECS_DCMU_P700_filename is None):
        print("No ECS_DCMU_P700 file for " + folder)
        return None
    ECS_DCMU_P700_data = pd.read_table(folder + ECS_DCMU_P700_filename, header=None)
    ECS_DCMU_P700_data.drop([4], axis=1, inplace=True)
    ECS_DCMU_P700_data.columns = ['Time', 'Fluorescence', 'Reference', 'Delta']
    ECS_DCMU_P700_data = ECS_DCMU_P700_data[[0, 3]]
    ECS_DCMU_P700_df = pd.DataFrame(ECS_DCMU_P700_data)

    ECS_DCMU_P700_df['x_correct'] = ECS_DCMU_P700_df['Time'] - ECS_DCMU_P700_df['Time'].iloc[2499]
    ECS_DCMU_P700_df['y_correct'] = ECS_DCMU_P700_df['Delta'] - ECS_DCMU_P700_df['Delta'].iloc[2490:2499].mean(axis=0)
    ECS_DCMU_P700_df['y_initial'] = ECS_DCMU_P700_df['y_correct'].iloc[2490:2499].mean(axis=0)
    ECS_DCMU_P700_df['y_final'] = ECS_DCMU_P700_df['y_correct'].iloc[2685:2695].mean(axis=0)
    ECS_DCMU_P700_df['amplitude'] = ECS_DCMU_P700_df['y_final'] - ECS_DCMU_P700_df['y_initial']

    # ECS_DCMU_P700_df.to_csv(DestinationFolder + basename + "_" + 'ECS_DCMU_P700_raw.csv')
    return ECS_DCMU_P700_df


ECS_DIRK_suffix = "dcmu_ecs_0003.dat"
def parse_ECS_data(folder):
    ECS_DIRK_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(ECS_DIRK_suffix):
            ECS_DIRK_filename = filename
    if (ECS_DIRK_filename is None):
        print("No ECS_DIRK file for " + folder)
        return None
    ECS_DIRK_data = pd.read_table(folder + ECS_DIRK_filename, header=None)
    ECS_DIRK_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    ECS_DIRK_data = ECS_DIRK_data[[0, 3]]
    ECS_DIRK_data = pd.DataFrame(ECS_DIRK_data)
    ECS_DIRK_data['x_correct'] = ECS_DIRK_data['Time'] - ECS_DIRK_data['Time'][249]
    ECS_DIRK_data['y_correct'] = ECS_DIRK_data['Delta'] - ECS_DIRK_data['Delta'][249]
    ECS_DIRK_data['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
    ECS_DIRK_data['amplitude'] = ECS_DIRK_data['y_correct'].iloc[470:495].mean(axis=0)

    # ECS_DIRK_data.to_csv(DestinationFolder + basename + "_" + "ECS_DIRK_raw.csv")
    return ECS_DIRK_data


def ECS_DCMU_P700_rates_calc(ECS_DCMU_P700_df, rep):
    ESC_DCMU_P700_slope = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(8, 18):
        rates_dict = {}
        rates_dict['x_initial'] = ECS_DCMU_P700_df['x_correct'][2499]
        rates_dict['x_final'] = ECS_DCMU_P700_df['x_correct'][2500 + x]
        rates_dict['y_initial'] = ECS_DCMU_P700_df['y_correct'].iloc[2490:2499].mean(axis=0)
        rates_dict['y_final'] = ECS_DCMU_P700_df['y_correct'].iloc[2500 + x]
        ESC_DCMU_P700_slope = ESC_DCMU_P700_slope.append(rates_dict, ignore_index=True)

    ESC_DCMU_P700_slope['Rate'] = (ESC_DCMU_P700_slope['y_final'] - ESC_DCMU_P700_slope['y_initial']) / (
    ESC_DCMU_P700_slope['x_final'] - ESC_DCMU_P700_slope['x_initial'])

    values_dict = {}
    values_dict['rates_mean'] = ESC_DCMU_P700_slope['Rate'].mean()
    values_dict['rates_std_dev'] = ESC_DCMU_P700_slope['Rate'].std()
    values_dict['end_trace_mean'] = ECS_DCMU_P700_df['y_correct'].iloc[2685:2695].mean(axis=0)
    values_dict['end_trace_std_dev'] = ECS_DCMU_P700_df['y_correct'].iloc[2685:2695].std(axis=0)
    values_dict['y_initial'] = ECS_DCMU_P700_df['y_correct'].iloc[2490:2499].mean(axis=0)
    values_dict['amplitude'] =  values_dict['end_trace_mean'] - values_dict['y_initial']
    ECS_DCMU_P700_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    # mean = ESC_DCMU_P700_slope['Rate'].mean()
    # std_dev = ESC_DCMU_P700_slope['Rate'].std()
    # return ECS_DCMU_P700_calc_values_df, ESC_DCMU_P700_slope, mean, std_dev
    return ECS_DCMU_P700_calc_values_df

def ECS_rates_calculator(ECS_DIRK_data, rep):
    slope_df = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(10, 20):
        rates_dict = {}
        rates_dict['x_initial'] = ECS_DIRK_data['x_correct'][249]
        rates_dict['x_final'] = ECS_DIRK_data['x_correct'][250 + x]
        rates_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
        rates_dict['y_final'] = ECS_DIRK_data['y_correct'].iloc[249 + x:251 + x].mean(axis=0)
        slope_df = slope_df.append(rates_dict, ignore_index=True)

    slope_df['Rate'] = (slope_df['y_final'] - slope_df['y_initial']) / (slope_df['x_final'] - slope_df['x_initial'])

    values_dict = {}
    values_dict['rates_mean'] = slope_df['Rate'].mean()
    values_dict['rates_std_dev'] = slope_df['Rate'].std()
    values_dict['end_trace_mean'] = ECS_DIRK_data['y_correct'].iloc[470:495].mean(axis=0)
    values_dict['end_trace_std_dev'] = ECS_DIRK_data['y_correct'].iloc[470:495].std(axis=0)
    values_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
    values_dict['amplitude'] = values_dict['y_initial'] - values_dict['end_trace_mean']
    ECS_DIRK_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    # mean = slope_df['Rate'].mean()
    # std_dev = slope_df['Rate'].std()
    # return slope_df, ECS_DIRK_calc_values_df, mean, std_dev
    return ECS_DIRK_calc_values_df


def flr_calculator(WholeTrace, rep):
    """
    calculate F0, Fs, Fm, etc.  Returns a dataframe with one row
    """
    calc_dict = {}

    # Values
    calc_dict["F0"] = WholeTrace.iloc[98][2]
    calc_dict["Fm"] = WholeTrace['NormFluor'].iloc[99:198].quantile(q=0.98)
    calc_dict["Fs"] = WholeTrace['NormFluor'].iloc[687:697].mean(axis=0)
    calc_dict["Fm_prime"] = WholeTrace['NormFluor'].iloc[700:780].quantile(q=0.98)
    calc_dict["F0_prime"] = WholeTrace['NormFluor'].iloc[1187:1197].mean(axis=0)
    calc_dict["Fm_prime2"] = WholeTrace['NormFluor'].iloc[1305:1380].quantile(q=0.98)
    calc_dict["Fm_prime4"] = WholeTrace['NormFluor'].iloc[2500:2580].quantile(q=0.98)
    calc_dict["Fm_prime6"] = WholeTrace['NormFluor'].iloc[3700:3780].quantile(q=0.98)

    F0 = calc_dict["F0"]
    Fm = calc_dict["Fm"]
    Fs = calc_dict["Fs"]
    Fm_prime = calc_dict["Fm_prime"]
    F0_prime = calc_dict["F0_prime"]
    Fm_prime2 = calc_dict["Fm_prime2"]
    Fm_prime4 = calc_dict["Fm_prime4"]
    Fm_prime6 = calc_dict["Fm_prime6"]

    # Calculations
    calc_dict["Fv"] = Fm - F0
    calc_dict["FvFm"] = calc_dict["Fv"] / Fm
    calc_dict["NPQ"] = (Fm - Fm_prime) / Fm_prime
    calc_dict["qE"] = Fm_prime2 - Fm_prime
    calc_dict["qL"] = ((Fm_prime - Fs) / (Fm_prime - F0_prime)) * (F0_prime / Fs)
    calc_dict["qT"] = Fm_prime6 - Fm_prime4
    calc_dict["qP"] = (Fm_prime - Fs) / (Fm_prime - F0_prime)

    measurements = pd.DataFrame(calc_dict, index=["rep" + str(rep)])
    return measurements

Phi2_Filename_Suffix = "vo2_flr_0001.dat"
Fluor_Filename_Suffix = "flr_0001.dat"
def parse_phi2_fluor(folder):
    Phi2_Filename = None
    Fluor_Filename = None
    for filename in os.listdir(folder):
        if filename.endswith(Phi2_Filename_Suffix):
            Phi2_Filename = filename
        elif filename.endswith(Fluor_Filename_Suffix):
            Fluor_Filename = filename
    if (Phi2_Filename is None):
        print("No phi2 file for " + folder)
        return None
    if (Fluor_Filename is None):
        print("No fluorescence file for " + folder)
        return None
    Phi2_data =  pd.read_table(folder + Phi2_Filename)
    Phi2_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    Phi2_data = Phi2_data[[0, 1]]

    Fluor_data = pd.read_table(folder + Fluor_Filename)
    Fluor_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    Fluor_data = Fluor_data[[0, 1]]
    FvFm_Trace = pd.DataFrame(Fluor_data[:599])
    DarkRec_Trace = pd.DataFrame(Fluor_data[600:])

    T1 =(FvFm_Trace, Phi2_data, DarkRec_Trace)

    WholeTrace = pd.concat(T1)
    WholeTrace.reset_index(WholeTrace, inplace=True, drop=True)

    BaseLineCor = (WholeTrace['Fluorescence'] - 0.127)
    Norm_Val = BaseLineCor[90:98].mean(axis=0)
    NormFluor = BaseLineCor / Norm_Val
    WholeTrace['NormFluor'] = NormFluor
    WholeTrace['y_correct'] = WholeTrace['NormFluor']
    return WholeTrace

def get_path(rootFolder, sample, timepoint, rep):
    rel_path = sample + "/" + "hr" + str(timepoint) + "/" + "rep" + str(rep) + "/"
    folder = rootFolder + rel_path
    if not os.path.isdir(folder):
        print(folder + " does not exist")
        return None, None, None
    basename = sample + "_" + "hr" + str(timepoint) + "_" + "rep" + str(rep)
    return rel_path, basename, folder