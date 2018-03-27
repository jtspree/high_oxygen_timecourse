"""
INFO

Plot functions
"""

# LIBRARY

import matplotlib.pyplot as plt

# FUNCTIONS

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
    plt.savefig(DestinationFolder + basename + "_" + "ECS_plot.png")
    # plt.show()
    plt.clf()

def savePlot(WholeTrace, DestinationFolder, basename):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    y = WholeTrace['NormFluor']
    ax.plot(y)
    ax.set_ylim(0, 4)
    ax.set_ylabel("Fluorescence")
    ax.set_xlabel("")
    # plt.show()
    fig.savefig(DestinationFolder + basename + "_plot.png")
    plt.clf()

# Plot of avg and std dev for timepoint
def plot_avg_stddev(averagesDestination, all_reps_fluor, sample, timepoint):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.errorbar(all_reps_fluor.index, all_reps_fluor['average'], all_reps_fluor['std dev'], ecolor='red')
    ax.set_ylim(0, 4)
    ax.set_ylabel("Fluorescence")
    # plt.show()
    fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "avg_plot.png")
    plt.clf()

# Plot of all replicates for timepoint
def plot_allreps(averagesDestination, all_reps_fluor, sample, timepoint, reps_list):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    for rep in reps_list:
        ax.plot(all_reps_fluor[rep], label='rep_' + str(rep))
    ax.set_ylim(0, 4)
    ax.legend()
    ax.set_ylabel("Fluorescence")
    # plt.show()
    fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "all_plot.png")
    plt.clf()