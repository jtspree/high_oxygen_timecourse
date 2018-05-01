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
    ECS_DIRK_data['y_correct'] = ECS_DIRK_data['Delta'] - ECS_DIRK_data['Delta'][240:249].mean(axis=0)
    ECS_DIRK_data['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
    ECS_DIRK_data['amplitude'] = ECS_DIRK_data['y_correct'].iloc[470:495].mean(axis=0)

    return ECS_DIRK_data


def ECS_rates_calculator(ECS_DIRK_data, sample, timepoint, rep, destination_folder):
    slope_df = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(10, 20):
        rates_dict = {}
        rates_dict['x_initial'] = ECS_DIRK_data['x_correct'][249]
        rates_dict['x_final'] = ECS_DIRK_data['x_correct'][250 + x]
        rates_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
        rates_dict['y_final'] = ECS_DIRK_data['y_correct'].iloc[249 + x:251 + x].mean(axis=0)
        slope_df = slope_df.append(rates_dict, ignore_index=True)

    slope_df['Rate'] = (slope_df['y_final'] - slope_df['y_initial']) / (slope_df['x_final'] - slope_df['x_initial'])
    slope_df.to_csv(destination_folder + '/{0}_hr{1}_rep{2}_ECS_DIRK_slopes.csv'.format(sample, timepoint, rep))

    values_dict = {}
    values_dict['ECS_DIRK_rates_mean'] = slope_df['Rate'].mean()
    values_dict['rates_std_dev'] = slope_df['Rate'].std()
    values_dict['end_trace_mean'] = ECS_DIRK_data['y_correct'].iloc[470:495].mean(axis=0)
    values_dict['end_trace_std_dev'] = ECS_DIRK_data['y_correct'].iloc[470:495].std(axis=0)
    values_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
    values_dict['ECS_DIRK_amplitude'] = values_dict['y_initial'] - values_dict['end_trace_mean']
    ECS_DIRK_calc_values_df = pd.DataFrame(values_dict, index=["rep" + str(rep)])

    return ECS_DIRK_calc_values_df


# save ECS DIRK plot
def save_ECS_DIRK_plot(destination_folder, basename, ECS_DIRK_data, mean):
    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = ECS_DIRK_data['x_correct']
    y1 = ECS_DIRK_data['y_correct']
    y2 = ECS_DIRK_data['y_initial']
    y3 = mean * x + ECS_DIRK_data['y_initial'][0]
    y4 = ECS_DIRK_data['amplitude']
    ax.set_xlim(-0.1, 1)
    ax.set_ylim(-0.001, 0.001)
    plt.plot(x, y1, label='signal')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='slope')
    plt.plot(x, y4, label='amplitude')
    plt.legend()
    plt.savefig(destination_folder + basename + "_" + "DCMU_ECS_DIRK_plot.png")
    plt.clf()