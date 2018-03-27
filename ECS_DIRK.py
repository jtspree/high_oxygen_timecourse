"""
INFO

Script for analyzing ECS DIRK data and generating plots

Created by Joshua Temple
Created 2018-03-26

@jtspree
"""

# LIBRARY

import plots
import parse_math

# CODE


# filepaths
ECS_DIRK_filename = "2017-08-14_cc1009_rep1_-hr0_dcmu_ecs_0003.dat"
FilePath = "C:/Users/templejo/Desktop/PBRexp060_PyScript/specdata_raw/CC-1009/hr0/rep1/"

ECS_DIRK_suffix = "dcmu_ecs_0003.dat"
DestinationFolder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/"
rootFolder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/specdata_raw/"

# parse ECS data into dataframe
ECS_DIRK_data = parse_math.parse_ECS_data(FilePath, ECS_DIRK_filename, DestinationFolder)

# calculate rates
df, values, mean, std_dev = parse_math.ECS_rates_calculator(ECS_DIRK_data, DestinationFolder)

# save ECS plot
plots.save_ECS_DIRK_plot(DestinationFolder, ECS_DIRK_data, mean)