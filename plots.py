"""
INFO

Functions to plot various flr, ECS data

Created by Joshua Temple
Assistance from Oliver Tessmer

Created 2018-03-27

@jtspree
"""

# LIBRARY

import matplotlib.pyplot as plt
import pandas as pd
import os

# FUNCTIONS


# save ECS DCMU P700 plot
def save_ECS_DCMU_P700_plot(destination_folder, basename, ECS_DCMU_P700_df, ECS_DCMU_P700_mean):
    fig = plt.figure(1, figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    x = ECS_DCMU_P700_df['x_correct']
    y1 = ECS_DCMU_P700_df['y_correct']
    y2 = ECS_DCMU_P700_df['y_initial']
    y3 = ECS_DCMU_P700_df['y_final']
    y4 = ECS_DCMU_P700_mean * x + ECS_DCMU_P700_df['y_initial'][0]
    ax.set_xlim(-0.1, 1)
    ax.set_ylim((ECS_DCMU_P700_df['y_initial'].mean() - 0.00005), (ECS_DCMU_P700_df['y_final'].mean() * 1.3))
    plt.plot(x, y1, label='ECS')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='y_final')
    plt.plot(x, y4, label='slope')
    plt.legend()
    plt.savefig(destination_folder + basename + "_" + 'DCMU_ECS_FIRK_rereduct_plot.png')
    plt.clf()


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
    plt.plot(x, y1, label='ECS')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='slope')
    plt.plot(x, y4, label='amplitude')
    plt.legend()
    plt.savefig(destination_folder + basename + "_" + "DCMU_ECS_DIRK_plot.png")
    plt.clf()


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


def save_allreps_plots(output_path_prefix, all_reps_combined_df, reps_list, xlim=None, ylim=None, ignore_index=False):
    # plot of average of reps
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.errorbar(
        range(len(all_reps_combined_df.index)) if ignore_index else all_reps_combined_df.index,
        all_reps_combined_df['average'], all_reps_combined_df['std dev'], ecolor='red')
    if xlim is not None:
        ax.set_xlim(xlim[0], xlim[1])
    if ylim is not None:
        ax.set_ylim(ylim[0], ylim[1])
    fig.savefig(output_path_prefix + '_avg_plot.png')
    plt.clf()

    # plot all replicates
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    for rep in reps_list:
        ax.plot(
            range(len(all_reps_combined_df.index)) if ignore_index else all_reps_combined_df.index,
            all_reps_combined_df[rep], label='rep_' + str(rep))
    if xlim is not None:
        ax.set_xlim(xlim[0], xlim[1])
    if ylim is not None:
        ax.set_ylim(ylim[0], ylim[1])
    ax.legend()
    fig.savefig(output_path_prefix + "_all_plot.png")
    plt.clf()


calc_values_dict = {
    # calc_value: [y_lim]
    'FvFm': (0, 1),
    'phi2': (0, None),
    'NPQ': (0, 1),
    'qE': (0, 1),
    'qI': (0, 1),
    'qL': (0, 1),
    'qP': (0, 1),
    'qT': (0, 1),
    'ECS_DIRK_amplitude': (0, None),
    'ECS_DIRK_rates_mean': (None, None),
    'ECS_DCMU_P700_amplitude': (0, None),
    'ECS_DCMU_P700_rates_mean': (None, None),
    'P700_DCMU_FIRK_oxidation_amplitude': (None, None),
    'P700_DCMU_FIRK_oxidation_rate_mean': (None, None),
    'vO2_ECS_DIRK_oxidation_amplitude': (None, None),
    'vO2_ECS_DIRK_oxidation_rate_mean': (None, None),
    'vO2_ECS_DIRK_rereduct_amplitude': (None, None),
    'vO2_ECS_DIRK_rereduct_rate_mean': (None, None)
}


def save_calc_values_plots(master_df, root_master_plots_folder, all_samples):
    missing_calc_values = list(calc_values_dict.keys())
    for col_index in range(2, len(master_df.columns), 2):
        col_name = master_df.columns[col_index][:-4]
        if col_name in calc_values_dict.keys():
            missing_calc_values.remove(col_name)
            fig = plt.figure(1)
            fig.set_figheight(5)
            fig.set_figwidth(5)
            ax = fig.add_subplot(1, 1, 1)
            for sample in master_df['sample'].unique():
                sample_df = master_df[master_df['sample'] == sample]
                avgs = sample_df.iloc[:, col_index]
                std_dev = sample_df.iloc[:, col_index+1]
                timepoint = sample_df['timepoint']
                ax.errorbar(timepoint, pd.to_numeric(avgs, errors='coerce'), pd.to_numeric(std_dev, errors='coerce'),
                            color=all_samples[sample][0], label=sample, marker='o', capsize=3)
            ax.set_xlabel('Timepoint (hours)', fontsize=14)
            # ax.set_ylabel(col_name, fontsize=14)
            ax.set_ylim(calc_values_dict[col_name])
            plt.title(col_name)
            ax.legend()
            fig.savefig(root_master_plots_folder + '/' + col_name + '.png')
            plt.clf()

    if len(missing_calc_values) > 0:
        raise Exception('missing calculated values from calc_values_list: ' + str(missing_calc_values))


def compare_samples_plot(all_samples_raw_trace, all_samples, all_timepoints, all_measurements_types, root_output):

    for timepoint in all_timepoints:

        path = root_output + '/compare' + '/' + "hr" + str(timepoint) + "/"
        if not os.path.isdir(path):
            os.makedirs(path)
        for measurement_type in all_measurements_types:

            xlim = all_measurements_types[measurement_type][2]
            ylim = all_measurements_types[measurement_type][3]
            ignore_index = all_measurements_types[measurement_type][4]

            line_count = 0
            fig = plt.figure(1, figsize=(10, 6))
            ax = fig.add_subplot(1, 1, 1)
            for sample in all_samples.keys():

                try:
                    y = all_samples_raw_trace[sample][timepoint][measurement_type]['average'].values
                except:
                    continue

                if ignore_index:
                    x = range(len(y))
                else:
                    x = all_samples_raw_trace[sample][timepoint][measurement_type].index

                line_count = line_count + 1
                ax.plot(x, y, label=sample, color=all_samples[sample][0])

            # if y trace less than 2, do not make graph
            if line_count < 2:
                continue

            # set axis limits & parameters
            if xlim is not None:
                ax.set_xlim(xlim[0], xlim[1])
            if ylim is not None:
                ax.set_ylim(ylim[0], ylim[1])
            ax.set_xlabel('Time (s)', fontsize=12)
            ax.set_ylabel('Delta A', fontsize=12)
            ax.tick_params('y', labelsize=8)
            plt.title(measurement_type)

            ax.legend()
            plt.tight_layout()
            fig.savefig(path + '/' + 'hr' + str(timepoint) + '_' + measurement_type + '.png')
            plt.clf()