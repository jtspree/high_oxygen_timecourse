"""
INFO

Contains functions to generate data, plots for
ECS DIRK data at start of trace

Created by Joshua Temple

Created 2018-04-03

@jtspree
"""

# LIBRARY

import pandas as pd
import os
import matplotlib.pyplot as plt

# CODE

# parse ECS_DIRK_starting data
ECS_DIRK_start_suffix = "dcmu_p700_0005.dat"
def parse_ECS_DIRK_start_data(folder):
    ECS_DIRK_start_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(ECS_DIRK_start_suffix):
            ECS_DIRK_start_filename = filename
    if (ECS_DIRK_start_filename is None):
        print("No ECS_DIRK_start file for " + folder)
        return None

    # generate dataframe for ECS_DIRK_start data
    ECS_DIRK_start_data = pd.read_table(folder + ECS_DIRK_start_filename, header=None)
    ECS_DIRK_start_data.drop([1, 2, 4], axis=1, inplace=True)
    ECS_DIRK_start_data.columns = ['Time', 'Delta']
    ECS_DIRK_start_df = pd.DataFrame(ECS_DIRK_start_data)

    ECS_DIRK_start_df['x_correct'] = ECS_DIRK_start_df['Time'] - ECS_DIRK_start_df['Time'].iloc[499]
    ECS_DIRK_start_df['y_correct'] = ECS_DIRK_start_df['Delta'] - ECS_DIRK_start_df['Delta'].iloc[479:499].mean(axis=0)
    ECS_DIRK_start_df['y_initial'] = ECS_DIRK_start_df['y_correct'].iloc[479:499].mean(axis=0)
    ECS_DIRK_start_df['y_final'] = ECS_DIRK_start_df['y_correct'].iloc[1000:1100].mean(axis=0)
    # amplitude is absolute value
    ECS_DIRK_start_df['amplitude'] = (ECS_DIRK_start_df['y_final'] - ECS_DIRK_start_df['y_initial']).abs()

    return ECS_DIRK_start_df