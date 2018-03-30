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


def ECS_DCMU_P700_rates_calc(ECS_DCMU_P700_df, sample, timepoint, rep, DestinationFolder):
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
    ESC_DCMU_P700_slope.to_csv(DestinationFolder + '/{0}_hr{1}_rep{2}_ECS_DCMU_P700_slopes.csv'.format(sample, timepoint, rep))

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

def ECS_rates_calculator(ECS_DIRK_data, sample, timepoint, rep, DestinationFolder ):
    slope_df = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(10, 20):
        rates_dict = {}
        rates_dict['x_initial'] = ECS_DIRK_data['x_correct'][249]
        rates_dict['x_final'] = ECS_DIRK_data['x_correct'][250 + x]
        rates_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
        rates_dict['y_final'] = ECS_DIRK_data['y_correct'].iloc[249 + x:251 + x].mean(axis=0)
        slope_df = slope_df.append(rates_dict, ignore_index=True)

    slope_df['Rate'] = (slope_df['y_final'] - slope_df['y_initial']) / (slope_df['x_final'] - slope_df['x_initial'])
    slope_df.to_csv(DestinationFolder + '/{0}_hr{1}_rep{2}_ECS_DIRK_slopes.csv'.format(sample, timepoint, rep))


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


def flr_calculator(whole_trace, sample, timepoint, rep, DestinationFolder):
    """
    calculate F0, Fs, Fm, etc.  Returns dataframe with one row
    """
    calc_dict = {}

    # FvFm1 values
    calc_dict["FvFm1_F0"] = whole_trace.iloc[98][2]
    calc_dict["FvFm1_Fm"] = whole_trace['y_correct'].iloc[105:185].quantile(q=0.98)
    calc_dict["FvFm1_Fs"] = whole_trace['y_correct'].iloc[585:595].mean(axis=0)

    # FvFm2 values

    calc_dict["FvFm2_F0"] = whole_trace['y_correct'].iloc[685:695].mean(axis=0)
    calc_dict["FvFm2_Fm"] = whole_trace['y_correct'].iloc[705:785].quantile(q=0.98)
    calc_dict["FvFm2_Fs"] = whole_trace['y_correct'].iloc[1185:1195].mean(axis=0)

    # phi2 values
    calc_dict["phi2_Fs"] = whole_trace['y_correct'].iloc[1288:1298].mean(axis=0)
    calc_dict["phi2_Fm"] = whole_trace['y_correct'].iloc[1300:1395].quantile(q=0.98)
    calc_dict["phi2_F0"] = whole_trace['y_correct'].iloc[1785:1795].mean(axis=0)

    # dark recovery, no FR
    calc_dict["darkrec_noFR_1_F0"] = whole_trace['y_correct'].iloc[1885:1895].mean(axis=0)
    calc_dict["darkrec_noFR_1_Fm"] = whole_trace['y_correct'].iloc[1905:1985].quantile(q=0.98)
    calc_dict["darkrec_noFR_1_Fs"] = whole_trace['y_correct'].iloc[2385:2395].mean(axis=0)

    calc_dict["darkrec_noFR_2_F0"] = whole_trace['y_correct'].iloc[2485:2495].mean(axis=0)
    calc_dict["darkrec_noFR_2_Fm"] = whole_trace['y_correct'].iloc[2505:2585].quantile(q=0.98)
    calc_dict["darkrec_noFR_2_Fs"] = whole_trace['y_correct'].iloc[2985:2995].mean(axis=0)

    calc_dict["darkrec_noFR_3_F0"] = whole_trace['y_correct'].iloc[3085:3095].mean(axis=0)
    calc_dict["darkrec_noFR_3_Fm"] = whole_trace['y_correct'].iloc[3105:3185].quantile(q=0.98)
    calc_dict["darkrec_noFR_3_Fs"] = whole_trace['y_correct'].iloc[3585:3595].mean(axis=0)

    # dark recovery, FR
    calc_dict["darkrec_FR_1_F0"] = whole_trace['y_correct'].iloc[3685:3695].mean(axis=0)
    calc_dict["darkrec_FR_1_Fm"] = whole_trace['y_correct'].iloc[3705:3785].quantile(q=0.98)
    calc_dict["darkrec_FR_1_Fs"] = whole_trace['y_correct'].iloc[4185:4195].mean(axis=0)

    calc_dict["darkrec_FR_2_F0"] = whole_trace['y_correct'].iloc[4285:4295].mean(axis=0)
    calc_dict["darkrec_FR_2_Fm"] = whole_trace['y_correct'].iloc[4305:4385].quantile(q=0.98)
    calc_dict["darkrec_FR_2_Fs"] = whole_trace['y_correct'].iloc[4785:4795].mean(axis=0)

    calc_dict["darkrec_FR_3_F0"] = whole_trace['y_correct'].iloc[4885:4895].mean(axis=0)
    calc_dict["darkrec_FR_3_Fm"] = whole_trace['y_correct'].iloc[4905:4985].quantile(q=0.98)
    calc_dict["darkrec_FR_3_Fs"] = whole_trace['y_correct'].iloc[5385:5395].mean(axis=0)

    # # Values
    # calc_dict["F0"] = whole_trace.iloc[98][2]
    # calc_dict["Fm"] = whole_trace['y_correct'].iloc[99:198].quantile(q=0.98)
    # calc_dict["Fs"] = whole_trace['y_correct'].iloc[687:697].mean(axis=0)
    # calc_dict["Fm_prime"] = whole_trace['y_correct'].iloc[700:780].quantile(q=0.98)
    # calc_dict["F0_prime"] = whole_trace['y_correct'].iloc[1187:1197].mean(axis=0)
    # calc_dict["Fm_prime2"] = whole_trace['y_correct'].iloc[1305:1380].quantile(q=0.98)
    # calc_dict["Fm_prime4"] = whole_trace['y_correct'].iloc[2500:2580].quantile(q=0.98)
    # calc_dict["Fm_prime6"] = whole_trace['y_correct'].iloc[3700:3780].quantile(q=0.98)
    #
    # F0 = calc_dict["F0"]
    # Fm = calc_dict["Fm"]
    # Fs = calc_dict["Fs"]
    # Fm_prime = calc_dict["Fm_prime"]
    # F0_prime = calc_dict["F0_prime"]
    # Fm_prime2 = calc_dict["Fm_prime2"]
    # Fm_prime4 = calc_dict["Fm_prime4"]
    # Fm_prime6 = calc_dict["Fm_prime6"]
    #
    # # Calculations
    # calc_dict["Fv"] = Fm - F0
    # calc_dict["FvFm"] = calc_dict["Fv"] / Fm
    # calc_dict["NPQ"] = (Fm - Fm_prime) / Fm_prime
    # calc_dict["qE"] = Fm_prime2 - Fm_prime
    # calc_dict["qL"] = ((Fm_prime - Fs) / (Fm_prime - F0_prime)) * (F0_prime / Fs)
    # calc_dict["qT"] = Fm_prime6 - Fm_prime4
    # calc_dict["qP"] = (Fm_prime - Fs) / (Fm_prime - F0_prime)
    # calc_dict['qI'] = (Fm - Fm_prime6) / Fm

    measurements = pd.DataFrame(calc_dict, index=["rep" + str(rep)])
    return measurements

phi2_filename_suffix = "vo2_flr_0001.dat"
flr_filename_suffix = "flr_0001.dat"
def parse_phi2_fluor(folder):
    phi2_filename = None
    flr_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(phi2_filename_suffix):
            phi2_filename = filename
        elif filename.endswith(flr_filename_suffix):
            flr_filename = filename
    if (phi2_filename is None):
        print("No phi2 file for " + folder)
        return None
    if (flr_filename is None):
        print("No fluorescence file for " + folder)
        return None
    phi2_data = pd.read_table(folder + phi2_filename)
    phi2_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    phi2_data = phi2_data[[0, 1]]

    flr_data = pd.read_table(folder + flr_filename)
    flr_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    flr_data = flr_data[[0, 1]]
    FvFm_Trace = pd.DataFrame(flr_data[:1199])
    dark_rec_trace = pd.DataFrame(flr_data[1200:])

    T1 =(FvFm_Trace, phi2_data, dark_rec_trace)

    whole_trace = pd.concat(T1)
    whole_trace.reset_index(whole_trace, inplace=True, drop=True)

    baseline_correction = (whole_trace['Fluorescence'] - 0.127)
    norm_value = baseline_correction[90:98].mean(axis=0)
    flr_norm = baseline_correction / norm_value
    whole_trace['y_correct'] = flr_norm
    return whole_trace

def get_path(rootFolder, sample, timepoint, rep):
    rel_path = sample + "/" + "hr" + str(timepoint) + "/" + "rep" + str(rep) + "/"
    folder = rootFolder + rel_path
    if not os.path.isdir(folder):
        print(folder + " does not exist")
        return None, None, None
    basename = sample + "_" + "hr" + str(timepoint) + "_" + "rep" + str(rep)
    return rel_path, basename, folder

def build_master_df(master_dict, all_samples, all_timepoints, all_measurements_types):
    master_df = pd.DataFrame()

    row_index = 0
    master_df['sample'] = ''
    master_df['timepoint'] = ''

    for sample in all_samples:
        for timepoint in all_timepoints:
            master_df.loc[row_index, 'sample'] = sample
            master_df.loc[row_index, 'timepoint'] = timepoint

            for measurements_type in all_measurements_types.keys():
                df = master_dict[sample][timepoint][measurements_type]
                for column in df.columns:
                    avg = df.loc['average', column]
                    std_dev = df.loc['std dev', column]
                    output_avg_col_name = column + '_' + 'avg'
                    output_stddev_col_name = column + '_' + 'stddev'
                    if output_avg_col_name not in master_df.columns:
                        master_df[output_avg_col_name] = ''
                    if output_stddev_col_name not in master_df.columns:
                        master_df[output_stddev_col_name] = ''
                    master_df.loc[row_index, output_avg_col_name] = avg
                    master_df.loc[row_index, output_stddev_col_name] = std_dev
            row_index = row_index + 1
    return master_df