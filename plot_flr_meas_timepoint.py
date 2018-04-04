"""
INFO

Created by Joshua Temple
Assistance from Oliver Tessmer

Created 2018-04-03

#jtspree
"""

# LIBRARY

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# PLOT SETTINGS

# 1 subplot per figure column and figure row

# x-axis tick labels of all subplots and corresponding input column name prefixes
x_axis = [98, 695, 1298, 1895, 2495, 3095, 3695, 4295, 4895]

# figure settings
x_lim = (0, 5000)
y_lim = (0, 4)
fig_height = 12
fig_width = 6
alpha = 0.3
linestyle = {"linestyle": "-", "linewidth": 2, "markeredgewidth": 4, "elinewidth": 2, "capsize": 2}

# colors for a row of boxes at the top of each subplot
# indicates the light environment
# dict: [box_color, box_text, box_text_color]
box_plot_dict = {
    'dark': ['black', 'dark', 'white'],
    'light': ['yellow', '1000', 'black'],
    'far_red': ['red', 'FR', 'white']
}
# box plot order and start positions
# must use box_plot_dictkeys
box_order = ['far_red', 'dark', 'light', 'dark', 'far_red']
box_start_x_pos = [0, 400, 1000, 1600, 3400]

measurement_prefix = ['FvFm1', 'FvFm2', 'phi2',
                      'darkrec_noFR_1', 'darkrec_noFR_2', 'darkrec_noFR_3',
                      'darkrec_FR_1', 'darkrec_FR_2', 'darkrec_FR_3']

# every sublot will contain 1 line per measurement suffix (input column name suffixes)
measurement_suffix = ['F0', 'Fm', 'Fs']


def save_flr_measurement_plot(master_df, root_master_folder, figure_rows, figure_columns):
    fig = plt.figure()
    fig.set_figwidth(fig_width)
    fig.set_figheight(fig_height)

    i = 1
    for timepoint in figure_rows:
        for sample in figure_columns:

            relavent_row_df = master_df[(master_df['sample'] == sample) & (master_df['timepoint'] == timepoint)]
            ax = fig.add_subplot(len(figure_rows), len(figure_columns), i)
            i = i + 1

            if timepoint == figure_rows[0]:
                ax.set_title(sample, fontsize=14)

            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)

            if timepoint == figure_rows[-1]:
                ax.set_xlabel('time (s)', fontsize=16)
            else:
                ax.set_xticks([])
                ax.set_xticklabels([])

            if sample == figure_columns[0]:
                ax.set_ylabel('hr' + str(timepoint), fontsize=16)
            else:
                ax.set_yticks([])
                ax.set_yticklabels([])

            for x_tick in x_axis:
                ax.axvline(x_tick, linewidth=0.2, color='black', linestyle=':')

            for y_tick in range(y_lim[0], y_lim[1]):
                ax.axhline(y_tick, linewidth=0.2, color='black', linestyle=':')

            for measurement in measurement_suffix:
                y_avg = []
                y_error = []
                for value in measurement_prefix:
                    input_col_name = value + '_' + measurement
                    y_avg.append(relavent_row_df[input_col_name + '_avg'].values[0])
                    y_error.append(relavent_row_df[input_col_name + '_stddev'].values[0])
                ax.errorbar(x_axis, y_avg, y_error, **linestyle, label=measurement)

            # places boxes on top of subplot
            for index, key in enumerate(box_order):
                box_specs = box_plot_dict[key]
                x = box_start_x_pos[index]
                width = (box_start_x_pos[index + 1] - x) if (index < len(box_order) - 1) else (x_lim[1] - x)
                ax.add_patch(patches.Rectangle(
                    (x, (y_lim[0])), width=width, height=(y_lim[1] - y_lim[0]), color=box_specs[0], alpha=alpha))
                ax.text(x + 0.5 * width, y_lim[1] - 0.25, box_specs[1],
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=8, color=box_specs[2])

            if (sample == figure_columns[-1]) and (timepoint == figure_rows[0]):
                ax.legend(prop={'size': 5})

    fig.tight_layout()
    fig.savefig(root_master_folder + '/' + 'flr_measurements_plot.png')
    fig.clf()