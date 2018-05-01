"""
INFO

DCMU ECS DIRK trace, calculator, plot script

Created by Joshua Temple
Created 2018-05-01

@jtspree
"""

# LIBRARY

import pandas as pd
import os
import matplotlib.pyplot as plt

# CODE

# parse P700_DCMU_ECS_rereduction data
P700_DCMU_ECS_rereduction_suffix = "dcmu_p700_0005.dat"
def parse_P700_DCMU_ECS_rereduction_data(folder):
    P700_DCMU_ECS_rereduction_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(P700_DCMU_ECS_rereduction_suffix):
            P700_DCMU_ECS_rereduction_filename = filename
    if (P700_DCMU_ECS_rereduction_filename is None):
        print("No P700_DCMU_ECS_rereduction file for " + folder)
        return None
    P700_DCMU_ECS_rereduction_data = pd.read_table(folder + P700_DCMU_ECS_rereduction_filename, header=None)
    P700_DCMU_ECS_rereduction_data.drop([4], axis=1, inplace=True)
    P700_DCMU_ECS_rereduction_data.columns = ['Time', 'Fluorescence', 'Reference', 'Delta']
    P700_DCMU_ECS_rereduction_data = P700_DCMU_ECS_rereduction_data[[0, 3]]
    P700_DCMU_ECS_rereduction_df = pd.DataFrame(P700_DCMU_ECS_rereduction_data)

    P700_DCMU_ECS_rereduction_df['x_correct'] = P700_DCMU_ECS_rereduction_df['Time'] - P700_DCMU_ECS_rereduction_df['Time'].iloc[2499]
    P700_DCMU_ECS_rereduction_df['y_correct'] = P700_DCMU_ECS_rereduction_df['Delta'] - P700_DCMU_ECS_rereduction_df['Delta'].iloc[2490:2499].mean(axis=0)
    P700_DCMU_ECS_rereduction_df['y_initial'] = P700_DCMU_ECS_rereduction_df['y_correct'].iloc[2490:2499].mean(axis=0)
    P700_DCMU_ECS_rereduction_df['y_final'] = P700_DCMU_ECS_rereduction_df['y_correct'].iloc[2685:2695].mean(axis=0)
    P700_DCMU_ECS_rereduction_df['amplitude'] = P700_DCMU_ECS_rereduction_df['y_final'] - P700_DCMU_ECS_rereduction_df['y_initial']

    return P700_DCMU_ECS_rereduction_df


def P700_DCMU_ECS_rereduction_rates_calc(P700_DCMU_ECS_rereduction_df, sample, timepoint, rep, destination_folder):
    P700_DCMU_ECS_rereduction_slope = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(8, 18):
        rates_dict = {}
        rates_dict['x_initial'] = P700_DCMU_ECS_rereduction_df['x_correct'][2499]
        rates_dict['x_final'] = P700_DCMU_ECS_rereduction_df['x_correct'][2500 + x]
        rates_dict['y_initial'] = P700_DCMU_ECS_rereduction_df['y_correct'].iloc[2490:2499].mean(axis=0)
        rates_dict['y_final'] = P700_DCMU_ECS_rereduction_df['y_correct'].iloc[2500 + x]
        P700_DCMU_ECS_rereduction_slope = P700_DCMU_ECS_rereduction_slope.append(rates_dict, ignore_index=True)

    P700_DCMU_ECS_rereduction_slope['rate'] = (P700_DCMU_ECS_rereduction_slope['y_final'] - P700_DCMU_ECS_rereduction_slope['y_initial']) / (
    P700_DCMU_ECS_rereduction_slope['x_final'] - P700_DCMU_ECS_rereduction_slope['x_initial'])
    P700_DCMU_ECS_rereduction_slope.to_csv(destination_folder +
                               '/{0}_hr{1}_rep{2}_P700_ECS_FIRK_rereduction_slopes.csv'.format(sample, timepoint, rep))

    values_dict = {}
    values_dict['P700_DCMU_ECS_rereduction_initial_slope'] = P700_DCMU_ECS_rereduction_slope['rate'].mean()
    values_dict['rates_std_dev'] = P700_DCMU_ECS_rereduction_slope['rate'].std()
    values_dict['end_trace_mean'] = P700_DCMU_ECS_rereduction_df['y_correct'].iloc[2685:2695].mean(axis=0)
    values_dict['end_trace_std_dev'] = P700_DCMU_ECS_rereduction_df['y_correct'].iloc[2685:2695].std(axis=0)
    values_dict['y_initial'] = P700_DCMU_ECS_rereduction_df['y_correct'].iloc[2490:2499].mean(axis=0)
    values_dict['P700_DCMU_ECS_rereduction_amplitude'] = values_dict['end_trace_mean'] - values_dict['y_initial']
    P700_DCMU_ECS_rereduction_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    return P700_DCMU_ECS_rereduction_calc_values_df


# save ECS DCMU P700 plot
def save_ECS_DCMU_P700_plot(destination_folder, basename, P700_DCMU_ECS_rereduction_df, P700_DCMU_ECS_rereduction_mean):
    fig = plt.figure(1, figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    x = P700_DCMU_ECS_rereduction_df['x_correct']
    y1 = P700_DCMU_ECS_rereduction_df['y_correct']
    y2 = P700_DCMU_ECS_rereduction_df['y_initial']
    y3 = P700_DCMU_ECS_rereduction_df['y_final']
    y4 = P700_DCMU_ECS_rereduction_mean * x + P700_DCMU_ECS_rereduction_df['y_initial'][0]
    ax.set_xlim(-0.1, 1)
    ax.set_ylim((P700_DCMU_ECS_rereduction_df['y_initial'].mean() - 0.00005), (P700_DCMU_ECS_rereduction_df['y_final'].mean() * 1.3))
    plt.plot(x, y1, label='signal')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='y_final')
    plt.plot(x, y4, label='slope')
    plt.title('P700_DCMU_ECS_rereduction')
    plt.legend()
    plt.savefig(destination_folder + basename + "_" + 'DCMU_ECS_FIRK_rereduction_plot.png')
    plt.clf()