"""
INFO

Plot functions
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
    ax.set_ylim((ECS_DCMU_P700_df['y_initial'].mean() - 0.00005), (ECS_DCMU_P700_df['y_final'].mean() * 1.2))
    plt.plot(x, y1, label='ECS')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='y_final')
    plt.plot(x, y4, label='slope')
    plt.legend()
    plt.savefig(DestinationFolder + basename + "_" +  'ECS_DCMU_P700_plot.png')


# save ECS DIRK plot
def save_ECS_DIRK_plot(DestinationFolder, basename, ECS_DIRK_data, mean):
    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = ECS_DIRK_data['x_correct']
    y1 = ECS_DIRK_data['y_correct']
    y2 = ECS_DIRK_data['y_initial']
    y3 = mean * x + ECS_DIRK_data['y_initial'][0]
    y4 = ECS_DIRK_data['amplitude']
    ax.set_ylim(-0.0008, 0.0008)
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
    y = WholeTrace['NormFluor']
    ax.plot(y)
    ax.set_ylim(0, 4)
    ax.set_ylabel("Fluorescence")
    ax.set_xlabel("")
    fig.savefig(DestinationFolder + basename + "_" + "flr_plot.png")
    plt.clf()

# plot of flr avg and std dev for timepoint
def plot_flr_avg(averagesDestination, all_reps_fluor, sample, timepoint):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.errorbar(all_reps_fluor.index, all_reps_fluor['average'], all_reps_fluor['std dev'], ecolor='red')
    ax.set_ylim(0, 4)
    ax.set_ylabel("Fluorescence")
    fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_avg_plot.png")
    plt.clf()

# plot of all flr replicates for timepoint
def plot_flr_allreps(averagesDestination, all_reps_fluor, sample, timepoint, reps_list):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    for rep in reps_list:
        ax.plot(all_reps_fluor[rep], label='rep_' + str(rep))
    ax.set_ylim(0, 4)
    ax.legend()
    ax.set_ylabel("Fluorescence")
    fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_all_plot.png")
    plt.clf()

# plot ECS DIRK avg and std dev for timepoint
def plot_ECS_DIRK_avg(averagesDestination, all_reps_ECS_DIRK, sample, timepoint):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.errorbar(all_reps_ECS_DIRK.index, all_reps_ECS_DIRK['average'], all_reps_ECS_DIRK['std dev'], ecolor='red')
    ax.set_ylim(-0.0008, 0.0008)
    fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DIRK_avg_plot.png")
    plt.clf()

# plot of all ECS DIRK replicates for timepoint
def plot_ECS_DIRK_allreps(averagesDestination, all_reps_ECS_DIRK, sample, timepoint, reps_list):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    for rep in reps_list:
        ax.plot(all_reps_ECS_DIRK[rep], label='rep_' + str(rep))
    ax.set_ylim(-0.0008, 0.0008)
    ax.legend()
    fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DIRK_all_plot.png")
    plt.clf()