"""
INFO

flourescence and phi2 parser, generate trace, calculator, plot script

Created by Joshua Temple
Created 2018-05-01

@jtspree
"""

# LIBRARY

import pandas as pd
import os
import matplotlib.pyplot as plt

# CODE

phi2_filename_suffix = "vo2_flr_0001.dat"
flr_filename_suffix = "flr_0001.dat"
def parse_phi2_flr(folder):
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


def flr_calculator(whole_trace, sample, timepoint, rep, destination_folder):
    # calculate F0, Fs, Fm, etc.  Returns dataframe with one row

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

    # calc_dict to use variables

    # FvFm1 values
    FvFm1_F0 = calc_dict["FvFm1_F0"]
    FvFm1_Fm = calc_dict["FvFm1_Fm"]
    FvFm1_Fs = calc_dict["FvFm1_Fs"]

    # FvFm2 values
    FvFm2_F0 = calc_dict["FvFm2_F0"]
    FvFm2_Fm = calc_dict["FvFm2_Fm"]
    FvFm2_Fs = calc_dict["FvFm2_Fs"]

    # phi2 values
    phi2_Fs = calc_dict["phi2_Fs"]
    phi2_Fm = calc_dict["phi2_Fm"]
    phi2_F0 = calc_dict["phi2_F0"]

    # dark recovery, no FR
    darkrec_noFR_1_F0 = calc_dict["darkrec_noFR_1_F0"]
    darkrec_noFR_1_Fm = calc_dict["darkrec_noFR_1_Fm"]
    darkrec_noFR_1_Fs = calc_dict["darkrec_noFR_1_Fs"]

    darkrec_noFR_2_F0 = calc_dict["darkrec_noFR_2_F0"]
    darkrec_noFR_2_Fm = calc_dict["darkrec_noFR_2_Fm"]
    darkrec_noFR_2_Fs = calc_dict["darkrec_noFR_2_Fs"]

    darkrec_noFR_3_F0 = calc_dict["darkrec_noFR_3_F0"]
    darkrec_noFR_3_Fm = calc_dict["darkrec_noFR_3_Fm"]
    darkrec_noFR_3_Fs = calc_dict["darkrec_noFR_3_Fs"]

    # dark recovery, FR
    darkrec_FR_1_F0 = calc_dict["darkrec_FR_1_F0"]
    darkrec_FR_1_Fm = calc_dict["darkrec_FR_1_Fm"]
    darkrec_FR_1_Fs = calc_dict["darkrec_FR_1_Fs"]

    darkrec_FR_2_F0 = calc_dict["darkrec_FR_2_F0"]
    darkrec_FR_2_Fm = calc_dict["darkrec_FR_2_Fm"]
    darkrec_FR_2_Fs = calc_dict["darkrec_FR_2_Fs"]

    darkrec_FR_3_F0 = calc_dict["darkrec_FR_3_F0"]
    darkrec_FR_3_Fm = calc_dict["darkrec_FR_3_Fm"]
    darkrec_FR_3_Fs = calc_dict["darkrec_FR_3_Fs"]

    # calculations

    calc_dict["Fv"] = FvFm1_Fm - FvFm1_F0
    calc_dict["FvFm"] = calc_dict["Fv"] / FvFm1_Fm
    calc_dict['phi2'] = (phi2_Fm - phi2_Fs) / phi2_Fm
    calc_dict["NPQ"] = (FvFm1_Fm - phi2_Fm) / phi2_Fm
    calc_dict["qE"] = darkrec_noFR_1_Fm - phi2_Fm
    calc_dict["qL"] = ((phi2_Fm - phi2_Fs) / (phi2_Fm - phi2_F0)) * (phi2_F0 / phi2_Fs)
    calc_dict["qT"] = (darkrec_FR_2_Fm - darkrec_noFR_3_Fm) / darkrec_noFR_3_Fm
    calc_dict["qP"] = (phi2_Fm - phi2_Fs) / (phi2_Fm - phi2_F0)
    calc_dict['qI'] = (FvFm1_Fm - darkrec_FR_2_Fm) / FvFm1_Fm

    measurements = pd.DataFrame(calc_dict, index=["rep" + str(rep)])
    return measurements


# save plot of flr trace
def save_flr_plot(WholeTrace, destination_folder, basename):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    y = WholeTrace['y_correct']
    ax.plot(y)
    ax.set_ylim(0, 4)
    ax.set_ylabel("Fluorescence")
    ax.set_xlabel("")
    fig.savefig(destination_folder + basename + "_" + "flr_plot.png")
    plt.clf()