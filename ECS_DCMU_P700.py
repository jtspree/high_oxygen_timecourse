"""
INFO

ECS DCMU P700 raw data analysis script
"""

# LIBRARY

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plots
import parse_math

# CODE

folder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/specdata_raw/CC-1009/hr0/rep1/"
ECS_P700_filename = '2017-08-14_cc1009_rep1_-hr0_dcmu_p700_0005.dat'
DestinationFolder = 'C:/Users/templejo/Desktop/PBRexp060_PyScript/'

ECS_DCMU_P700_df = parse_math.parse_ECS_DCMU_P700_data(folder, DestinationFolder, ECS_P700_filename)

ESC_DCMU_P700_slope, mean, std_dev = parse_math.ECS_DCMU_P700_rates_calc(ECS_DCMU_P700_df)

# save ECS DCMU P700 plot
plots.save_ECS_DCMU_P700_plot(DestinationFolder, ECS_DCMU_P700_df, mean)