"""
INFO

ECS DCMU P700 raw data analysis script
"""

# LIBRARY

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plots

# CODE

folder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/specdata_raw/CC-1009/hr0/rep1/"
ECS_P700_filename = '2017-08-14_cc1009_rep1_-hr0_dcmu_p700_0005.dat'
DestinationFolder = 'C:/Users/templejo/Desktop/PBRexp060_PyScript/'


ECS_DCMU_P700_data = pd.read_table(folder + ECS_P700_filename, header=None)
ECS_DCMU_P700_df = pd.DataFrame(ECS_DCMU_P700_data)
ECS_DCMU_P700_df.drop([4], axis=1, inplace=True)
ECS_DCMU_P700_df.columns = ['Time', 'Fluorescence', 'Reference', 'Delta']
ECS_DCMU_P700_df = ECS_DCMU_P700_df[[0, 3]]

ECS_DCMU_P700_df['x_correct'] = ECS_DCMU_P700_df['Time'] - ECS_DCMU_P700_df['Time'].iloc[2499]
ECS_DCMU_P700_df['y_correct'] = ECS_DCMU_P700_df['Delta'] - ECS_DCMU_P700_df['Delta'].iloc[2490:2499].mean(axis=0)
ECS_DCMU_P700_df['y_initial'] = ECS_DCMU_P700_df['y_correct'].iloc[2490:2499].mean(axis=0)
ECS_DCMU_P700_df['y_final'] = ECS_DCMU_P700_df['y_correct'].iloc[2556:2565].mean(axis=0)
ECS_DCMU_P700_df['amplitude'] = ECS_DCMU_P700_df['y_final'] - ECS_DCMU_P700_df['y_initial']


ESC_DCMU_P700_slope = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
for x in range(8, 18):
    rates_dict = {}
    rates_dict['x_initial'] = ECS_DCMU_P700_df['x_correct'][2499]
    rates_dict['x_final'] = ECS_DCMU_P700_df['x_correct'][2500 + x]
    rates_dict['y_initial'] = ECS_DCMU_P700_df['y_correct'].iloc[2490:2499].mean(axis=0)
    rates_dict['y_final'] = ECS_DCMU_P700_df['y_correct'].iloc[2500 + x]
    ESC_DCMU_P700_slope = ESC_DCMU_P700_slope.append(rates_dict, ignore_index=True)

ESC_DCMU_P700_slope['Rate'] = (ESC_DCMU_P700_slope['y_final'] - ESC_DCMU_P700_slope['y_initial']) / (ESC_DCMU_P700_slope['x_final'] - ESC_DCMU_P700_slope['x_initial'])

mean = ESC_DCMU_P700_slope['Rate'].mean()
std_dev = ESC_DCMU_P700_slope['Rate'].std()

# save ECS DCMU P700 plot
plots.save_ECS_DCMU_P700_plot(DestinationFolder, ECS_DCMU_P700_df, mean)