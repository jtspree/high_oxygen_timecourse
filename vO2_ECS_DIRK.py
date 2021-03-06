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
vO2_ECS_DIRK_suffix = "vo2_ecs_0003.dat"
def parse_vO2_ECS_DIRK_oxidation_data(folder):
    vO2_ECS_DIRK_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(vO2_ECS_DIRK_suffix):
            vO2_ECS_DIRK_filename = filename
    if (vO2_ECS_DIRK_filename is None):
        print("No vO2_ECS_DIRK_oxidation file for " + folder)
        return None

    # generate dataframe for ECS_DIRK_start data
    vO2_ECS_DIRK_data = pd.read_table(folder + vO2_ECS_DIRK_filename, header=None)
    vO2_ECS_DIRK_data.drop([1, 2], axis=1, inplace=True)
    vO2_ECS_DIRK_data.columns = ['Time', 'Delta']
    vO2_ECS_DIRK_df = pd.DataFrame(vO2_ECS_DIRK_data)

    vO2_ECS_DIRK_df['x_correct'] = vO2_ECS_DIRK_df['Time'] - vO2_ECS_DIRK_df['Time'].iloc[249]
    vO2_ECS_DIRK_df['y_correct'] = vO2_ECS_DIRK_df['Delta'] - vO2_ECS_DIRK_df['Delta'].iloc[239:249].mean(axis=0)
    vO2_ECS_DIRK_df['y_initial'] = vO2_ECS_DIRK_df['y_correct'].iloc[239:249].mean(axis=0)
    vO2_ECS_DIRK_df['y_final'] = vO2_ECS_DIRK_df['y_correct'].iloc[280:300].mean(axis=0)
    # amplitude is absolute value
    vO2_ECS_DIRK_df['amplitude'] = (vO2_ECS_DIRK_df['y_final'] - vO2_ECS_DIRK_df['y_initial']).abs()

    return vO2_ECS_DIRK_df


def vO2_ECS_DIRK_rates_calc(vO2_ECS_DIRK_df, sample, timepoint, rep, destination_folder):
    vO2_ECS_DIRK_slope = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(2, 7):
        rates_dict = {}
        rates_dict['x_initial'] = vO2_ECS_DIRK_df['x_correct'][249]
        rates_dict['x_final'] = vO2_ECS_DIRK_df['x_correct'][249 + x]
        rates_dict['y_initial'] = vO2_ECS_DIRK_df['y_correct'].iloc[239:249].mean(axis=0)
        rates_dict['y_final'] = vO2_ECS_DIRK_df['y_correct'].iloc[249 + x]
        vO2_ECS_DIRK_slope = vO2_ECS_DIRK_slope.append(rates_dict, ignore_index=True)

    vO2_ECS_DIRK_slope['rate'] = ((vO2_ECS_DIRK_slope['y_final'] - vO2_ECS_DIRK_slope['y_initial'])
                                / (vO2_ECS_DIRK_slope['x_final'] - vO2_ECS_DIRK_slope['x_initial']))
    vO2_ECS_DIRK_slope.to_csv(destination_folder + '/{0}_hr{1}_rep{2}_vO2_ECS_DIRK_slopes.csv'.format(sample, timepoint, rep))

    values_dict = {}
    values_dict['vO2_ECS_DIRK_initial_slope'] = vO2_ECS_DIRK_slope['rate'].mean()
    values_dict['vO2_ECS_DIRK_initial_slope'] = abs(values_dict['vO2_ECS_DIRK_initial_slope'])
    values_dict['v02_ECS_DIRK_std_dev'] = vO2_ECS_DIRK_slope['rate'].std()
    values_dict['end_trace_mean'] = vO2_ECS_DIRK_df['y_correct'].iloc[280:300].mean(axis=0)
    values_dict['end_trace_std_dev'] = vO2_ECS_DIRK_df['y_correct'].iloc[280:300].std(axis=0)
    values_dict['y_initial'] = vO2_ECS_DIRK_df['y_correct'].iloc[239:249].mean(axis=0)
    values_dict['vO2_ECS_DIRK_amplitude'] = (values_dict['y_initial'] - values_dict['end_trace_mean'])
    vO2_ECS_DIRK_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    return vO2_ECS_DIRK_calc_values_df


def save_vO2_ECS_DIRK_plot(destination_folder, basename, vO2_ECS_DIRK_df, vO2_ECS_DIRK_mean):
    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = vO2_ECS_DIRK_df['x_correct']
    y1 = vO2_ECS_DIRK_df['y_correct']
    y2 = vO2_ECS_DIRK_df['y_initial']
    y3 = vO2_ECS_DIRK_df['y_final']
    y4 = (vO2_ECS_DIRK_mean * -1) * x + vO2_ECS_DIRK_df['y_initial'][0]
    ax.set_xlim(-0.1, 0.2)
    ax.set_ylim(-0.002, 0.0004)
    plt.plot(x, y1, label='signal')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='y_final')
    plt.plot(x, y4, label='slope')
    plt.title('vO2_ECS_DIRK')
    plt.legend()
    plt.savefig(destination_folder + basename + "_" + 'vO2_ECS_DIRK_plot.png')
    plt.clf()