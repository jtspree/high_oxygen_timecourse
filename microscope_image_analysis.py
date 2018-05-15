"""
INFO

Analyzes microscope image analysis data
Generates graphs and stats

Created by Joshua Temple
Created 2018-05-15

@jtspree
"""

# LIBRARY

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# LISTS

ecotype_list = ['CC-1009', 'CC-2343']
timepoint_list = [0, 1, 3, 6, 12, 24, 48]
rep_list = [1, 2, 3, 4]


# FUNCTIONS


def stats_by_timepoint(data_type):

    grouped_df = stats_by_groups(['ecotype', 'timepoint'], data_type)

    filler_list = []
    for ecotype in ecotype_list:
        for timepoint in timepoint_list:
            filler = ecotype, timepoint
            filler_list.append(filler)
    filler_df = pd.DataFrame(filler_list, columns=['ecotype', 'timepoint'])

    merged_df = pd.merge(filler_df, grouped_df, how='left', left_on=['ecotype', 'timepoint'],
                         right_on=['ecotype', 'timepoint'])
    merged_df['count'].fillna(0, inplace=True)

    return merged_df


def stats_by_reps(data_type):

    grouped_df = stats_by_groups(['ecotype', 'timepoint', 'rep'], data_type)

    filler_list = []
    for ecotype in ecotype_list:
        for timepoint in timepoint_list:
            for rep in rep_list:
                filler = ecotype, timepoint, rep
                filler_list.append(filler)
    filler_df = pd.DataFrame(filler_list, columns=['ecotype', 'timepoint', 'rep'])

    merged_df = pd.merge(filler_df, grouped_df, how='left', left_on=['ecotype', 'timepoint', 'rep'],
                         right_on=['ecotype', 'timepoint', 'rep'])
    merged_df['count'].fillna(0, inplace=True)

    return merged_df


def stats_by_groups(grouped_columns, data_type):

    # define a pandas 'groupby' object which will be used for several different statistics
    groups = microscope_data_df.groupby(grouped_columns)

    # create a dataframe with all the grouped_columns, and a "count" for each group
    grouped_df = groups.size().reset_index(name='count')

    # add new col with statistics
    # col name must be pandas stats function
    for new_col in ["min", "max", "mean", "std", ['quantile', 0.25], ['quantile', 0.75]]:
        if type(new_col) == list:
            grouped_df[new_col[0] + ' ' + str(new_col[1])] = getattr(groups[data_type], new_col[0])(new_col[1]).values
        else:
            grouped_df[new_col] = getattr(groups[data_type], new_col)().values

    return grouped_df


# CODE

if __name__ == "__main__":
    print("microscope_image_analysis.py is being run directly")
else:
    raise Exception('Do not use in another module')

# location for microscope data
folder_microscope = 'C:/Users/templejo/Desktop/high_oxygen_timecourse/microscope_images/'
microscope_compiled_data = 'microscope_compiled.xlsx'

# create dataframe with compiled microscope data
microscope_data = pd.read_excel(folder_microscope + microscope_compiled_data)
microscope_data_df = pd.DataFrame(microscope_data)

# create violin plot figure

# plot settings
fig, ax = plt.subplots()
fig.set_size_inches(16, 12)

# create seaborn violin plot
ax = sns.violinplot(x="timepoint", y="volume", hue="ecotype",
                    data=microscope_data_df, palette="muted", split=True,
                    inner='quartile')

# plot axis settings
ax.set_ylim(-200, 1500)
ax.set_ylabel('Volume (fL)')
ax.set_xlabel('High Oxygen (hours)')
# plt.show()

for data_type in ['area', 'perimeter', 'volume']:

    stats_by_timepoint(data_type).to_csv(folder_microscope + '/' + 'timepoint_stats_' + data_type + '.csv')
    stats_by_reps(data_type).to_csv(folder_microscope + '/' + 'rep_stats_' + data_type + '.csv')