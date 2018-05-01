"""
INFO

Functions to parse various flr, ECS data

Created by Joshua Temple
Assistance from Oliver Tessmer

Created 2018-03-27

@jtspree
"""

# LIBRARY

import pandas as pd
import os

# FUNCTION


def get_path(root_folder, sample, timepoint, rep):
    rel_path = sample + "/" + "hr" + str(timepoint) + "/" + "rep" + str(rep) + "/"
    folder = root_folder + rel_path
    if not os.path.isdir(folder):
        print(folder + " does not exist")
        return None, None, None
    basename = sample + "_" + "hr" + str(timepoint) + "_" + "rep" + str(rep)
    return rel_path, basename, folder

def build_master_df(master_dict, all_samples, all_timepoints, all_measurements_types):
    master_df = pd.DataFrame()

    row_index = 0
    master_df['sample'] = float('NaN')
    master_df['timepoint'] = float('NaN')

    for sample in all_samples:
        for timepoint in all_timepoints:
            master_df.loc[row_index, 'sample'] = sample
            master_df.loc[row_index, 'timepoint'] = timepoint

            for measurements_type in all_measurements_types.keys():
                if measurements_type not in master_dict[sample][timepoint].keys():
                    continue
                df = master_dict[sample][timepoint][measurements_type]
                for column in df.columns:
                    avg = df.loc['average', column]
                    std_dev = df.loc['std dev', column]
                    output_avg_col_name = column + '_' + 'avg'
                    output_stddev_col_name = column + '_' + 'stddev'
                    if output_avg_col_name not in master_df.columns:
                        master_df[output_avg_col_name] = ''
                    if output_stddev_col_name not in master_df.columns:
                        master_df[output_stddev_col_name] = ''
                    master_df.loc[row_index, output_avg_col_name] = avg
                    master_df.loc[row_index, output_stddev_col_name] = std_dev
            row_index = row_index + 1
    return master_df