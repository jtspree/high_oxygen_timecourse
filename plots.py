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

# FUNCTIONS


# save ECS DCMU P700 plot
def save_ECS_DCMU_P700_plot(DestinationFolder, basename, ECS_DCMU_P700_df, ECS_DCMU_P700_mean):
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
    plt.savefig(DestinationFolder + basename + "_" + 'ECS_DCMU_P700_plot.png')
    plt.clf()


# save ECS DIRK plot
def save_ECS_DIRK_plot(DestinationFolder, basename, ECS_DIRK_data, mean):
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
    plt.savefig(DestinationFolder + basename + "_" + "ECS_DIRK_plot.png")
    plt.clf()


# save plot of flr trace
def save_flr_plot(WholeTrace, DestinationFolder, basename):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    y = WholeTrace['y_correct']
    ax.plot(y)
    ax.set_ylim(0, 4)
    ax.set_ylabel("Fluorescence")
    ax.set_xlabel("")
    fig.savefig(DestinationFolder + basename + "_" + "flr_plot.png")
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
    'ECS_DIRK_oxidation_amplitude': (None, None),
    'ECS_DIRK_oxidation_rate_mean': (None, None)
}


def save_calc_values_plots(master_df, root_master_plots_folder):
    missing_calc_values = list(calc_values_dict.keys())
    for col_index in range(2, len(master_df.columns), 2):
        col_name = master_df.columns[col_index][:-4]
        if col_name in calc_values_dict.keys():
            missing_calc_values.remove(col_name)
            fig = plt.figure(1, figsize=(10, 6))
            ax = fig.add_subplot(1, 1, 1)
            for sample in master_df['sample'].unique():
                sample_df = master_df[master_df['sample'] == sample]
                avgs = sample_df.iloc[:, col_index]
                std_dev = sample_df.iloc[:, col_index+1]
                timepoint = sample_df['timepoint']
                ax.errorbar(timepoint, avgs, std_dev, label=sample, marker='o', capsize=3)
            ax.set_xlabel('Timepoint (hours)', fontsize=14)
            ax.set_ylim(calc_values_dict[col_name])
            ax.legend()
            fig.savefig(root_master_plots_folder + '/' + col_name + '.png')
            plt.clf()
    if len(missing_calc_values) > 0:
        raise Exception('missing calculated values from calc_values_list: ' + str(missing_calc_values))