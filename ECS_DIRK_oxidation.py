"""
INFO

Contains functions to generate data, plots for
ECS DIRK oxidation data at start of trace

Created by Joshua Temple

Created 2018-04-03

@jtspree
"""

# LIBRARY

import pandas as pd
import os
import matplotlib.pyplot as plt

# CODE

# parse ECS_DIRK_starting data
ECS_DIRK_oxidation_suffix = "dcmu_p700_0005.dat"
def parse_ECS_DIRK_oxidation_data(folder):
    ECS_DIRK_oxidation_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(ECS_DIRK_oxidation_suffix):
            ECS_DIRK_oxidation_filename = filename
    if (ECS_DIRK_oxidation_filename is None):
        print("No ECS_DIRK_oxidation file for " + folder)
        return None

    # generate dataframe for ECS_DIRK_start data
    ECS_DIRK_oxidation_data = pd.read_table(folder + ECS_DIRK_oxidation_filename, header=None)
    ECS_DIRK_oxidation_data.drop([1, 2, 4], axis=1, inplace=True)
    ECS_DIRK_oxidation_data.columns = ['Time', 'Delta']
    ECS_DIRK_oxidation_df = pd.DataFrame(ECS_DIRK_oxidation_data)

    ECS_DIRK_oxidation_df['x_correct'] = ECS_DIRK_oxidation_df['Time'] - ECS_DIRK_oxidation_df['Time'].iloc[499]
    ECS_DIRK_oxidation_df['y_correct'] = ECS_DIRK_oxidation_df['Delta'] - ECS_DIRK_oxidation_df['Delta'].iloc[479:499].mean(axis=0)
    ECS_DIRK_oxidation_df['y_initial'] = ECS_DIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
    ECS_DIRK_oxidation_df['y_final'] = ECS_DIRK_oxidation_df['y_correct'].iloc[1000:1100].mean(axis=0)
    # amplitude is absolute value
    ECS_DIRK_oxidation_df['amplitude'] = (ECS_DIRK_oxidation_df['y_final'] - ECS_DIRK_oxidation_df['y_initial']).abs()

    return ECS_DIRK_oxidation_df


def ECS_DIRK_oxidation_rates_calc(ECS_DIRK_oxidation_df, sample, timepoint, rep, DestinationFolder):
    ECS_DIRK_oxidation_slope = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(2, 7):
        rates_dict = {}
        rates_dict['x_initial'] = ECS_DIRK_oxidation_df['x_correct'][499]
        rates_dict['x_final'] = ECS_DIRK_oxidation_df['x_correct'][499 + x]
        rates_dict['y_initial'] = ECS_DIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
        rates_dict['y_final'] = ECS_DIRK_oxidation_df['y_correct'].iloc[499 + x]
        ECS_DIRK_oxidation_slope = ECS_DIRK_oxidation_slope.append(rates_dict, ignore_index=True)

    ECS_DIRK_oxidation_slope['rate'] = ((ECS_DIRK_oxidation_slope['y_final'] - ECS_DIRK_oxidation_slope['y_initial'])
                                / (ECS_DIRK_oxidation_slope['x_final'] - ECS_DIRK_oxidation_slope['x_initial'])).abs()
    ECS_DIRK_oxidation_slope.to_csv(DestinationFolder + '/{0}_hr{1}_rep{2}_ECS_DIRK_oxidation_slopes.csv'.format(sample, timepoint, rep))

    values_dict = {}
    values_dict['ECS_DIRK_oxidation_rate_mean'] = ECS_DIRK_oxidation_slope['rate'].mean()
    values_dict['ECS_DIRK_oxidation_std_dev'] = ECS_DIRK_oxidation_slope['rate'].std()
    values_dict['end_trace_mean'] = ECS_DIRK_oxidation_df['y_correct'].iloc[1000:1100].mean(axis=0)
    values_dict['end_trace_std_dev'] = ECS_DIRK_oxidation_df['y_correct'].iloc[1000:1100].std(axis=0)
    values_dict['y_initial'] = ECS_DIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
    values_dict['ECS_DIRK_oxidation_amplitude'] = (values_dict['y_initial'] - values_dict['end_trace_mean'])
    ECS_DIRK_oxidation_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    return ECS_DIRK_oxidation_calc_values_df


def save_ECS_DIRK_oxidation_plot(DestinationFolder, basename, ECS_DIRK_oxidation_df, ECS_DIRK_oxidation_mean):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = ECS_DIRK_oxidation_df['x_correct']
    y1 = ECS_DIRK_oxidation_df['y_correct']
    y2 = ECS_DIRK_oxidation_df['y_initial']
    y3 = ECS_DIRK_oxidation_df['y_final']
    y4 = ECS_DIRK_oxidation_mean * x + ECS_DIRK_oxidation_df['y_initial'][0]
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.001, .0002)
    plt.plot(x, y1, label='ECS')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='y_final')
    plt.plot(x, y4, label='slope')
    plt.legend()
    plt.savefig(DestinationFolder + basename + "_" + 'ECS_DIRK_oxidation_plot.png')
    plt.clf()