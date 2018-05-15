"""
INFO

Script to analyze raw sample data
(ie. biomass, cell count, chlorophyll)

Created by Joshua Temple
Created 2018-05-09

@jtspree
"""

# LIBRARY

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# CODE

sample_folder = "C:/Users/templejo/Desktop/high_oxygen_timecourse/"
sample_file = 'raw_sample_data.xlsx'
sample_output = "C:/Users/templejo/Desktop/high_oxygen_timecourse/output/"

data = pd.read_excel(sample_folder + sample_file)
data_df = pd.DataFrame(data)
print(data_df)
