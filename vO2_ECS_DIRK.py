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
vO2_ECS_DIRK_oxidation_suffix = "vo2_ecs_0003.dat"
def parse_vO2_ECS_DIRK_oxidation_data(folder):
    vO2_ECS_DIRK_oxidation_filename = None
    for filename in os.listdir(folder):
        if filename.endswith(vO2_ECS_DIRK_oxidation_suffix):
            vO2_ECS_DIRK_oxidation_filename = filename
    if (vO2_ECS_DIRK_oxidation_filename is None):
        print("No vO2_ECS_DIRK_oxidation file for " + folder)
        return None

    # generate dataframe for ECS_DIRK_start data
    vO2_ECS_DIRK_oxidation_data = pd.read_table(folder + vO2_ECS_DIRK_oxidation_filename, header=None)
    vO2_ECS_DIRK_oxidation_data.drop([1, 2, 4], axis=1, inplace=True)
    vO2_ECS_DIRK_oxidation_data.columns = ['Time', 'Delta']
    vO2_ECS_DIRK_oxidation_df = pd.DataFrame(vO2_ECS_DIRK_oxidation_data)

    vO2_ECS_DIRK_oxidation_df['x_correct'] = vO2_ECS_DIRK_oxidation_df['Time'] - vO2_ECS_DIRK_oxidation_df['Time'].iloc[499]
    vO2_ECS_DIRK_oxidation_df['y_correct'] = vO2_ECS_DIRK_oxidation_df['Delta'] - vO2_ECS_DIRK_oxidation_df['Delta'].iloc[479:499].mean(axis=0)
    vO2_ECS_DIRK_oxidation_df['y_initial'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[479:499].mean(axis=0)
    vO2_ECS_DIRK_oxidation_df['y_final'] = vO2_ECS_DIRK_oxidation_df['y_correct'].iloc[1000:1100].mean(axis=0)
    # amplitude is absolute value
    vO2_ECS_DIRK_oxidation_df['amplitude'] = (vO2_ECS_DIRK_oxidation_df['y_final'] - vO2_ECS_DIRK_oxidation_df['y_initial']).abs()

    return vO2_ECS_DIRK_oxidation_df