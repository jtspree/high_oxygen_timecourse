"""
INFO

Contains functions to generate data, plots for
vO2 ECS DIRK oxidation data at start of trace

Created by Joshua Temple

Created 2018-04-16

@jtspree
"""

# LIBRARY

import pandas as pd
import os
import matplotlib.pyplot as plt

# FUNCTIONS

# parse vO2_ECS_DIRK_oxidation data
vO2_ECS_DIRK_oxidation_suffix = "vo2_ecs_0003.dat"
def parse_vO2_ECS_DIRK_oxidation_data(folder):
    vO2_ECS_DIRK_oxidation_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(vO2_ECS_DIRK_oxidation_suffix):
            vO2_ECS_DIRK_oxidation_filename = filename
    if (vO2_ECS_DIRK_oxidation_filename is None):
        print("No vO2_ECS_DIRK_oxidation file for " + folder)
        return None

    # generate dataframe for ECS_DIRK_start data
    vO2_ECS_DIRK_oxidation_data = pd.read_table(folder + vO2_ECS_DIRK_oxidation_filename, header=None)
    vO2_ECS_DIRK_oxidation_data.drop([1, 2, 4], axis=1, inplace=True)
    vO2_ECS_DIRK_oxidation_data.columns = ['Time', 'Delta']
    vO2_ECS_DIRK_oxidation_df = pd.DataFrame(vO2_ECS_DIRK_oxidation_data)

    vO2_ECS_DIRK_oxidation_df['x_correct'] = vO2_ECS_DIRK_oxidation_df['Time'] - vO2_ECS_DIRK_oxidation_df['Time'].iloc[499]
    vO2_ECS_DIRK_oxidation_df['y_correct'] = vO2_ECS_DIRK_oxidation_df['Delta'] - vO2_ECS_DIRK_oxidation_df['Delta'].iloc[479:499].mean(axis=0)
    vO2_ECS_DIRK_oxidation_df['y_initial'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
    vO2_ECS_DIRK_oxidation_df['y_final'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[1000:1100].mean(axis=0)
    # amplitude is absolute value
    vO2_ECS_DIRK_oxidation_df['amplitude'] = (vO2_ECS_DIRK_oxidation_df['y_final'] - vO2_ECS_DIRK_oxidation_df['y_initial']).abs()

    return vO2_ECS_DIRK_oxidation_df


def ECS_DIRK_oxidation_rates_calc(vO2_ECS_DIRK_oxidation_df, sample, timepoint, rep, destination_folder):
    vO2_ECS_DIRK_oxidation_slope = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(2, 7):
        rates_dict = {}
        rates_dict['x_initial'] = vO2_ECS_DIRK_oxidation_df['x_correct'][499]
        rates_dict['x_final'] = vO2_ECS_DIRK_oxidation_df['x_correct'][499 + x]
        rates_dict['y_initial'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
        rates_dict['y_final'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[499 + x]
        vO2_ECS_DIRK_oxidation_slope = vO2_ECS_DIRK_oxidation_slope.append(rates_dict, ignore_index=True)

    vO2_ECS_DIRK_oxidation_slope['rate'] = ((vO2_ECS_DIRK_oxidation_slope['y_final'] - vO2_ECS_DIRK_oxidation_slope['y_initial'])
                                / (vO2_ECS_DIRK_oxidation_slope['x_final'] - vO2_ECS_DIRK_oxidation_slope['x_initial']))
    vO2_ECS_DIRK_oxidation_slope.to_csv(destination_folder + '/{0}_hr{1}_rep{2}_ECS_DIRK_oxidation_slopes.csv'.format(sample, timepoint, rep))

    values_dict = {}
    values_dict['ECS_DIRK_oxidation_rate_mean'] = vO2_ECS_DIRK_oxidation_slope['rate'].mean()
    values_dict['ECS_DIRK_oxidation_std_dev'] = vO2_ECS_DIRK_oxidation_slope['rate'].std()
    values_dict['end_trace_mean'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[1000:1100].mean(axis=0)
    values_dict['end_trace_std_dev'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[1000:1100].std(axis=0)
    values_dict['y_initial'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
    values_dict['ECS_DIRK_oxidation_amplitude'] = (values_dict['y_initial'] - values_dict['end_trace_mean'])
    vO2_ECS_DIRK_oxidation_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    return vO2_ECS_DIRK_oxidation_calc_values_df


def save_vO2_ECS_DIRK_oxidation_plot(destination_folder, basename, vO2_ECS_DIRK_oxidation_df, ECS_DIRK_oxidation_mean):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = vO2_ECS_DIRK_oxidation_df['x_correct']
    y1 = vO2_ECS_DIRK_oxidation_df['y_correct']
    y2 = vO2_ECS_DIRK_oxidation_df['y_initial']
    y3 = vO2_ECS_DIRK_oxidation_df['y_final']
    y4 = ECS_DIRK_oxidation_mean * x + vO2_ECS_DIRK_oxidation_df['y_initial'][0]
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.001, .0002)
    plt.plot(x, y1, label='ECS')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='y_final')
    plt.plot(x, y4, label='slope')
    plt.legend()
    plt.savefig(destination_folder + basename + "_" + 'vO2_ECS_DIRK_oxidation_plot.png')
    plt.clf()