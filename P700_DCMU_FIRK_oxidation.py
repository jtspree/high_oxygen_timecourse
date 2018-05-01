"""
INFO

Contains functions to generate data, plots for
P700_DCMU_FIRK_oxidation data at start of trace

Created by Joshua Temple

Created 2018-04-03

@jtspree
"""

# LIBRARY

import pandas as pd
import os
import matplotlib.pyplot as plt

# FUNCTIONS

# parse P700_DCMU_FIRK_oxidation data
P700_DCMU_FIRK_oxidation_suffix = "dcmu_p700_0005.dat"
def parse_P700_DCMU_FIRK_oxidation_data(folder):
    P700_DCMU_FIRK_oxidation_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(P700_DCMU_FIRK_oxidation_suffix):
            P700_DCMU_FIRK_oxidation_filename = filename
    if (P700_DCMU_FIRK_oxidation_filename is None):
        print("No P700_DCMU_FIRK_oxidation file for " + folder)
        return None

    # generate dataframe for P700_DCMU_FIRK_oxidation data
    P700_DCMU_FIRK_oxidation_data = pd.read_table(folder + P700_DCMU_FIRK_oxidation_filename, header=None)
    P700_DCMU_FIRK_oxidation_data.drop([1, 2, 4], axis=1, inplace=True)
    P700_DCMU_FIRK_oxidation_data.columns = ['Time', 'Delta']
    P700_DCMU_FIRK_oxidation_df = pd.DataFrame(P700_DCMU_FIRK_oxidation_data)

    P700_DCMU_FIRK_oxidation_df['x_correct'] = P700_DCMU_FIRK_oxidation_df['Time'] - P700_DCMU_FIRK_oxidation_df['Time'].iloc[499]
    P700_DCMU_FIRK_oxidation_df['y_correct'] = P700_DCMU_FIRK_oxidation_df['Delta'] - P700_DCMU_FIRK_oxidation_df['Delta'].iloc[479:499].mean(axis=0)
    P700_DCMU_FIRK_oxidation_df['y_initial'] = P700_DCMU_FIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
    P700_DCMU_FIRK_oxidation_df['y_final'] = P700_DCMU_FIRK_oxidation_df['y_correct'].iloc[1000:1100].mean(axis=0)
    # amplitude is absolute value
    P700_DCMU_FIRK_oxidation_df['amplitude'] = (P700_DCMU_FIRK_oxidation_df['y_final'] - P700_DCMU_FIRK_oxidation_df['y_initial']).abs()

    return P700_DCMU_FIRK_oxidation_df


def P700_DCMU_FIRK_oxidation_rates_calc(P700_DCMU_FIRK_oxidation_df, sample, timepoint, rep, destination_folder):
    P700_DCMU_FIRK_oxidation_slope = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(2, 7):
        rates_dict = {}
        rates_dict['x_initial'] = P700_DCMU_FIRK_oxidation_df['x_correct'][499]
        rates_dict['x_final'] = P700_DCMU_FIRK_oxidation_df['x_correct'][499 + x]
        rates_dict['y_initial'] = P700_DCMU_FIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
        rates_dict['y_final'] = P700_DCMU_FIRK_oxidation_df['y_correct'].iloc[499 + x]
        P700_DCMU_FIRK_oxidation_slope = P700_DCMU_FIRK_oxidation_slope.append(rates_dict, ignore_index=True)

    P700_DCMU_FIRK_oxidation_slope['rate'] = ((P700_DCMU_FIRK_oxidation_slope['y_final'] - P700_DCMU_FIRK_oxidation_slope['y_initial'])
                                / (P700_DCMU_FIRK_oxidation_slope['x_final'] - P700_DCMU_FIRK_oxidation_slope['x_initial']))
    P700_DCMU_FIRK_oxidation_slope.to_csv(destination_folder + '/{0}_hr{1}_rep{2}_P700_DCMU_FIRK_oxidation_slopes.csv'.format(sample, timepoint, rep))

    values_dict = {}
    values_dict['P700_DCMU_FIRK_oxidation_initial_slope'] = P700_DCMU_FIRK_oxidation_slope['rate'].mean()
    values_dict['P700_DCMU_FIRK_oxidation_initial_slope'] = abs(values_dict['P700_DCMU_FIRK_oxidation_initial_slope'])
    values_dict['P700_DCMU_FIRK_oxidation_std_dev'] = P700_DCMU_FIRK_oxidation_slope['rate'].std()
    values_dict['end_trace_mean'] = P700_DCMU_FIRK_oxidation_df['y_correct'].iloc[1000:1100].mean(axis=0)
    values_dict['end_trace_std_dev'] = P700_DCMU_FIRK_oxidation_df['y_correct'].iloc[1000:1100].std(axis=0)
    values_dict['y_initial'] = P700_DCMU_FIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
    values_dict['P700_DCMU_FIRK_oxidation_amplitude'] = (values_dict['y_initial'] - values_dict['end_trace_mean'])
    P700_DCMU_FIRK_oxidation_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    return P700_DCMU_FIRK_oxidation_calc_values_df


def save_P700_DCMU_FIRK_oxidation_plot(destination_folder, basename, P700_DCMU_FIRK_oxidation_df, P700_DCMU_FIRK_oxidation_mean):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = P700_DCMU_FIRK_oxidation_df['x_correct']
    y1 = P700_DCMU_FIRK_oxidation_df['y_correct']
    y2 = P700_DCMU_FIRK_oxidation_df['y_initial']
    y3 = P700_DCMU_FIRK_oxidation_df['y_final']
    y4 = (P700_DCMU_FIRK_oxidation_mean * -1) * x + P700_DCMU_FIRK_oxidation_df['y_initial'][0]
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.001, .0002)
    plt.plot(x, y1, label='signal')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='y_final')
    plt.plot(x, y4, label='slope')
    plt.legend()
    plt.savefig(destination_folder + basename + "_" + 'P700_DCMU_FIRK_oxidation_plot.png')
    plt.clf()