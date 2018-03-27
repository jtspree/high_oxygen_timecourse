"""
INFO
"""

# LIBRARY

import pandas as pd
import os

# FUNCTION

ECS_DIRK_suffix = "dcmu_ecs_0003.dat"
def parse_ECS_data(folder, DestinationFolder, basename):
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

    ECS_DIRK_data.to_csv(DestinationFolder + basename + "_" + "ECS_DIRK_raw.csv")
    return ECS_DIRK_data


def ECS_rates_calculator(ECS_DIRK_data, DestinationFolder, basename):
    df = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(10, 20):
        rates_dict = {}
        rates_dict['x_initial'] = ECS_DIRK_data['x_correct'][249]
        rates_dict['x_final'] = ECS_DIRK_data['x_correct'][250 + x]
        rates_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
        rates_dict['y_final'] = ECS_DIRK_data['y_correct'].iloc[249 + x:251 + x].mean(axis=0)
        df = df.append(rates_dict, ignore_index=True)

    df['Rate'] = (df['y_final'] - df['y_initial']) / (df['x_final'] - df['x_initial'])
    df.to_csv(DestinationFolder + basename + "_" + "ECS_DIRK_rates.csv")

    values = pd.DataFrame(columns=['rates_mean', 'rates_std_dev', 'end_trace_mean', 'end_trace_std_dev', 'y_initial', 'amplitude'])

    values_dict = {}
    values_dict['rates_mean'] = df['Rate'].mean()
    values_dict['rates_std_dev'] = df['Rate'].std()
    values_dict['end_trace_mean'] = ECS_DIRK_data['y_correct'].iloc[470:495].mean(axis=0)
    values_dict['end_trace_std_dev'] = ECS_DIRK_data['y_correct'].iloc[470:495].std(axis=0)
    values_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
    values_dict['amplitude'] = values_dict['y_initial'] - values_dict['end_trace_mean']
    values = values.append(values_dict, ignore_index=True)
    values.to_csv(DestinationFolder + basename + "_" + "ECS_DIRK_values.csv")

    mean = df['Rate'].mean()
    std_dev = df['Rate'].std()
    return df, values, mean, std_dev

def calculator(WholeTrace, rep):
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
    return WholeTrace

def get_path(rootFolder, sample, timepoint, rep):
    rel_path = sample + "/" + "hr" + str(timepoint) + "/" + "rep" + str(rep) + "/"
    folder = rootFolder + rel_path
    if not os.path.isdir(folder):
        print(folder + " does not exist")
        return None, None, None
    basename = sample + "_" + "hr" + str(timepoint) + "_" + "rep" + str(rep)
    return rel_path, basename, folder